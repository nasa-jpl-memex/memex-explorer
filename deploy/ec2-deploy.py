#!/usr/bin/env python
import os
import boto.exception
import boto.ec2
import time

from fabric.api import (
    env,
    settings,
    sudo,
    run,
)

from fabric.contrib.files import (
    comment,
    uncomment,
    exists,
    append,
    sed
)

import logging
#based on https://github.com/ContinuumIO/wakari-deploy/blob/master/ami_creation/fabfile.py

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)

# log.addHandler(handler)
log.addHandler(console)

AMI_ID = 'ami-f43b3e9c' #SSD in us-east-1

if 'xxx' == os.environ.get('AWS_ID').lower():
    print("you must pass a value for the environment variable AWS_ID")
    quit()
if 'xxx' == os.environ.get('AWS_SECRET').lower():
    print("you must pass a value for the environment variable AWS_SECRET")
    quit()

ec2 = boto.ec2.connect_to_region('us-east-1', 
        aws_access_key_id = os.environ.get('AWS_ID'),
        aws_secret_access_key = os.environ.get('AWS_SECRET'))
env.use_ssh_config = True
env.disable_known_hosts = True
env.connection_attempts = True
env.timeout = 40

def create_box():
    old_ids = set(i.id for i in ec2.get_only_instances())
    machine = ec2.run_instances(AMI_ID, key_name=AMI_ID+"-amfarrell", security_groups=['all-open',])
    new_instance = [i for i in ec2.get_only_instances() if i.id not in old_ids][0]
    #It is utterly inefficient and stupid to run through all of these.
    print new_instance.id
    while new_instance.state != u'running':
        time.sleep(3)
        new_instance.update()
    while ec2.get_all_instance_status(instance_ids=[new_instance.id])[0].system_status.details['reachability'] != 'passed':
        time.sleep(3)
    time.sleep(1)
    assert new_instance.public_dns_name
    print(new_instance.public_dns_name)
    return new_instance

def create_keypair(source = AMI_ID+'-amfarrell'):
    try:
        kp = ec2.delete_key_pair(source)
    except (boto.exception.EC2ResponseError):
        pass

    kp = ec2.create_key_pair(source)
    filename = os.environ.get('EC2_KEY_PATH', '/Users/afarrell/projects/memex-explorer/deploy/ec2.key')
    kfile = open(filename, 'wb')
    def file_mode(user, group, other):
        return user*(8**2) + group*(8**1) + other*(8**0)
    kfile.write(kp.material)
    kfile.close()
    os.chmod(filename, file_mode(7,0,0))
    return filename

def test_ssh(instance, key_file):
    # needed to convert from unicode to ascii?
    key_file = str(key_file)
    ip = str(instance.public_dns_name)
    env.host = 'ubuntu@e' + ip
    env.host_string = ip
    env.hosts = [env.host]
    env.user = 'ubuntu'
    env.key_file = key_file
    env.key_filename = key_file

    # forward ssh agent -- equivalent of ssh -A
    env.forward_agent = True

    log.info('Key file: %s' % (key_file))
    log.debug('Trying to connect...')
    run('pwd')


def apt_installs():
    log.info("installing packages with apt-get")
    sudo("add-apt-repository -y ppa:keithw/mosh")
    sudo("apt-get update -y")
    packages = [
        'nginx',
        'docker',
        'git',
        'silversearcher-ag',
        'python-software-properties',
        'mosh',
        'tig']
    sudo("apt-get install -y {}".format(' '.join(packages)))

def fix_sshd_config():
    '''root needs an actual shell, so fix the sshd_config.'''
    config_file = '/etc/ssh/sshd_config'
    uncomment(config_file, r'^.*PermitRootLogin yes', use_sudo=True)
    comment(config_file, r'^PermitRootLogin forced-commands-only', use_sudo=True)

def install_miniconda():
    url = 'http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh'
    run("wget {}".format(url))
    run("chmod +x ./Miniconda-latest-Linux-x86_64.sh")
    run("./Miniconda-latest-Linux-x86_64.sh")
    run("source .profile")

def install_repo():
    url = 'https://github.com/memex-explorer/memex-explorer/'
    run("git clone {}".format(url))
    run("cd memex-explorer")
    if os.environ.get('GIT_BRANCH'):
        with settings(warn_only=True):
            run("git checkout {}".format(os.environ.get('GIT_BRANCH')))
    run("source ~/.profile")
    run("conda env create")
    run("source activate memex")

MEMEX_APP_PORT = 8000
def start_nginx(instance):
    run("cd ~/memex-explorer/deploy")
    run("IP_ADDR='{ip}' AWS_DOMAIN='{domain}' ROOT_PORT='{port}' python generate_initial_nginx.py {template} {destination}".format(
        source = "../source/base/deploy_templates/nginx-reverse-proxy-conf.jinja2", destination="./initial_nginx.conf",
        ip=instance.ip_address, domain=instance.public_dns_name, port=MEMEX_APP_PORT))
    sudo("cp ./initial_nginx.conf /etc/nginx/sites-enabled/default")
    sudo("service nginx restart")

def start_server_running(instance):
    run("cd ~/memex-explorer")
    run("python source/manage.py migrate")
    run("python source/manage.py runserver {}:{} && disown".format(instance.ip_address, MEMEX_APP_PORT))



key_filename = create_keypair()
instance = create_box()
ssh_command = 'ssh -i {key} ubuntu@{ip} "'.format(ip=instance.ip_address, key=key_filename)
mosh_command = 'mosh ubuntu@{ip} --ssh="ssh -i {key}"'.format(ip=instance.ip_address, key=key_filename)
try:
    test_ssh(instance, key_filename)
    print(ssh_command)
    apt_installs()
    print(mosh_command)
    fix_sshd_config()
except Exception, e:
    import pdb;pdb.set_trace()
    print instance.public_dns_name
    print e
    ec2.terminate_instances([instance.id])
    raise e
#with open("~/.aliases", 'a') as f:
#  f.write("alias memex='{}'\n".format(ssh_command))
#  f.write("alias mosh_memex='{}'\n".format(mosh_command))
#  f.flush()
try:
    install_miniconda()
    install_repo()
    start_server_running(instance)
    print(instance.public_dns_name)
except Exception, e:
    print(ssh_command)
    print(mosh_command)
    raise e
