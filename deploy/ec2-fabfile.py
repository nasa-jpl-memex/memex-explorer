#!/usr/bin/env python
import os
import sys
import boto.exception
import boto.ec2
import datetime
import time
import subprocess

from fabric.api import (
    env,
    settings,
    sudo,
    prefix,
    cd,
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

MEMEX_APP_PORT = 8000
SETTINGS_FILENAME = '/vagrant/source/memex/local_settings.py'
HTPASSWD_FILENAME = '/vagrant/deploy/dot-htpasswd'

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

KEYNAME = "{}-{}".format(AMI_ID,os.environ.get('USER', 'memex'))

def create_box():
    old_ids = set(i.id for i in ec2.get_only_instances())
    machine = ec2.run_instances(AMI_ID, key_name=KEYNAME,
        security_groups=['all-open',], instance_type='m3.2xlarge')
    new_instance = [i for i in ec2.get_only_instances() if i.id not in old_ids][0]
    print(new_instance.id)
    while new_instance.state != u'running':
        time.sleep(3)
        new_instance.update()
    while ec2.get_all_instance_status(instance_ids=[new_instance.id])[0].system_status.details['reachability'] != 'passed':
        time.sleep(3)
    time.sleep(1)
    assert new_instance.public_dns_name
    print(new_instance.public_dns_name)
    return new_instance


def create_keypair(source = KEYNAME):
    try:
        kp = ec2.delete_key_pair(source)
    except (boto.exception.EC2ResponseError):
        pass

    kp = ec2.create_key_pair(source)
    filename = os.environ.get('EC2_KEY_PATH', './keys/ec2-{}.pem'.format(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')))
    latest_filename = os.environ.get('EC2_KEY_PATH', './keys/latest.pem')
    kfile = open(filename, 'wb')
    latest_kfile = open(latest_filename, 'wb')
    def file_mode(user, group, other):
        return user*(8**2) + group*(8**1) + other*(8**0)
    kfile.write(kp.material)
    latest_kfile.write(kp.material)
    kfile.close()
    latest_kfile.close()
    os.chmod(filename, file_mode(7,0,0))
    os.chmod(latest_filename, file_mode(7,0,0))
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

def connect_to_existing_machine(ip, key_file_path):
    env.user = 'ubuntu'
    env.hosts = ['{}@{}'.format(env.user, ip)]
    env.host = '{}@{}'.format(env.user, ip)
    env.host_string = '{}@{}'.format(env.user, ip)
    env.key_file = key_file_path
    env.key_filename = key_file_path
    env.forward_agent = True
    log.info('Key file: %s' % (key_file_path))
    log.debug('Trying to connect...')
    run('pwd')

def create_vagrant():
    #Not idempotent
    log.info("creating vagrant user")
    sudo("sudo id -u vagrant &>/dev/null || sudo useradd vagrant -m -G sudo -p '*' --shell /bin/bash")
    sudo("passwd -d vagrant")
    run("echo 'vagrant ALL=(ALL) NOPASSWD: ALL' | sudo tee /etc/sudoers.d/vagrant")
    sudo("cp -rf /home/ubuntu/.ssh /home/vagrant/.ssh")
    sudo("chown vagrant:vagrant /home/vagrant/.ssh")
    sudo("chown vagrant:vagrant /home/vagrant/.ssh/authorized_keys")
    env.user = 'vagrant'
    log.debug('Trying to connect as vagrant...')
    run('pwd')



def apt_installs():
    log.info("installing packages with apt-get")
    sudo("add-apt-repository -y ppa:saltstack/salt")
    sudo("apt-get update -y")
    packages = ['salt-master', 'salt-minion', 'salt-syndic', 'git', 'tig']
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
    run("./Miniconda-latest-Linux-x86_64.sh -b")
    run("echo 'export PATH=/home/ubuntu/miniconda/bin:\$PATH' >> ~/.bashrc")
    run("source ~/.bashrc")

def install_repo(public_dns_name, ip_address):
    sudo('rm -rf ~/memex-explorer')
    url = 'https://github.com/memex-explorer/memex-explorer/'
    if os.environ.get('GIT_BRANCH'):
        run("git clone {} --branch {}".format(url, os.environ.get('GIT_BRANCH')))
    else:
        run("git clone {}".format(url))
    sudo('rm -rf /vagrant')
    sudo('mv /home/vagrant/memex-explorer /vagrant')
    sudo('chown -R vagrant:vagrant /vagrant')
    sudo("find /vagrant -type f -name '*' -print0 | sudo xargs -0 chown vagrant:vagrant")
    sudo('ln -s /vagrant /home/vagrant/memex-explorer')
    run("echo 'HOSTNAME = \"{}\"' >> {}".format(public_dns_name, SETTINGS_FILENAME))
    run("echo 'ROOT_PORT = \"{}\"' >> {}".format(MEMEX_APP_PORT, SETTINGS_FILENAME))
    run("echo 'IP_ADDR = \"{}\"' >> {}".format(ip_address, SETTINGS_FILENAME))
    run("echo {} > {}".format(os.environ.get('HTPASSWD'), HTPASSWD_FILENAME))

def run_salt():
    sudo('mkdir -p /etc/salt')
    sudo('ln -f -s /vagrant/salt/deploy/minion /etc/salt/minion')
    sudo('ln -f -s /vagrant/salt/deploy/roots/salt /srv/salt')
    sudo('sudo /usr/bin/salt-call state.highstate --retcode-passthrough --log-level=debug | tee /home/vagrant/salt-log')

def convenience_aliases():
    run("echo 'alias dj=\"~/miniconda/bin/python ~/memex-explorer/source/manage.py\"' >> ~/.bashrc")


if os.environ.get('MEMEX_IP_ADDR'):
    ip_address = os.environ.get('MEMEX_IP_ADDR')
    key_filename = os.path.abspath('./keys/ec2-{}.pem'.format(ip_address))
    public_dns_name = 'ec2-{}.compute-1.amazonaws.com'.format(ip_address.replace('.','-'))
    connect_to_existing_machine(ip_address, key_filename)
else:
    key_filename = create_keypair()
    instance = create_box()
    subprocess.check_output(['cp', key_filename, 
                             os.path.join(os.path.dirname(key_filename), 'ec2-{}.pem'.format(instance.ip_address))])
    public_dns_name = instance.public_dns_name
    ip_address = instance.ip_address
    test_ssh(instance, key_filename)
ssh_command = 'ssh -i {key} ubuntu@{ip} "'.format(ip=ip_address, key=key_filename)
mosh_command = 'mosh ubuntu@{ip} --ssh="ssh -i {key}"'.format(ip=ip_address, key=key_filename)
if 'quitafterec2spinup' in sys.argv:
    print(ssh_command)
    quit()
try:
    print(ssh_command)
    apt_installs()
    print(mosh_command)
    fix_sshd_config()
except Exception:
    print("{} failed!".format(public_dns_name))
    if not os.environ.get('MEMEX_IP_ADDR'):
        ec2.terminate_instances([instance.id])
    raise
try:
    create_vagrant()
    install_miniconda()
    install_repo(public_dns_name, ip_address)
    run_salt()
except Exception:
    print(ssh_command)
    print(mosh_command)
    raise
