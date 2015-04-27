"""Base models."""

import os

from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse

from jinja2 import Template
from jinja2.runtime import Context

from django.conf import settings

from task_manager.file_tasks import unzip


def alphanumeric_validator():
    return RegexValidator(r'^[a-zA-Z0-9-_ ]+$',
        'Only numbers, letters, underscores, dashes and spaces are allowed.')

APPS = [
    {
        'name': 'web',
        'dockerfile' : ".",
        'command' : "python ./manage.py runserver 0.0.0.0:8000",
        'volumes': [("./source", "./source")],
        'expose' : [8000],
    }, {
        'name': 'solr',
        'dockerfile' : "./solr",
        'command' : "/workdir/solr_entry.sh",
        'volumes': [("./solr", "/workdir")],
        'expose': [8983, 5005,]
    }
]

def generate_docker_compose(new_slug, project_app_ports={}):
    project_slugs = list(Project.objects.values('slug')) + [{'slug': new_slug}],
    projects = []
    for slug in project_slugs:
       projects.append({'name': slug, apps:[]})
        projects[-1]
        for app in APPS:
            projects[-1]['apps'].append({
                'name': app['name'],
                'port': project_app_ports["{}{}".format(slug, app['name'])],
            })
    context = {
        'hostname' : 'structureandinterperetation.com',
        'root_port' : 8617,
        'projects' : projects,
    }
    compose_template = Template(open('/home/ubuntu/memex-explorer/deploy/docker-compose.yml.jinja2', 'r').read(),
                                trim_blocks = True, lstrip_blocks = True)
    compose_config = compose_template.render(trim_blocks = True, lstrip_blocks = True, **context)
    with open('/home/ubuntu/memex-explorer/docker-compose.yml', 'w') as f:
        f.write(compose_config)
        f.flush()
    return 'memexexplorer_{name}_run_{iteration}'

def generate_nginx_config(new_slug):
    context = {
        'hostname' : 'structureandinterperetation.com',
        'root_port' : 8617,
        'projects' : list(Project.objects.values('slug')) + [{'slug': new_slug}],
        'apps' : APPS
    }
    nginx_template = Template(open('/home/ubuntu/memex-explorer/deploy/nginx-reverse-proxy.conf.jinja2', 'r').read(),
                                trim_blocks = True, lstrip_blocks = True)
    nginx_config = nginx_template.render(**context)
    with open('/home/ubuntu/memex-explorer/nginx-reverse-proxy.conf', 'w') as f:
        f.write(nginx_config)
        f.flush()

def zipped_file_validator():
    return RegexValidator(r'.*\.(ZIP|zip)$',
        'Only compressed archive (.zip) files are allowed.')

class Project(models.Model):
    """Project model.

    Every application that plugs into Memex Explorer should have a
    foreign key relationship to a Project.

    Model Fields
    ------------

    name : str, 64 characters max
    slug : str, 64 characters max
        The `slug` field is derived from `name` on save, and is restricted
        to URL-safe characters.
    description : textfield

    """

    def get_zipped_data_path(self, filename):
        return os.path.join(settings.PROJECT_PATH, self.slug, "zipped_data", filename)

    def get_dumped_data_path(self):
        return os.path.join(settings.PROJECT_PATH, self.slug, "data")
    name = models.CharField(max_length=64, unique=True,
        validators=[alphanumeric_validator()])
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    uploaded_data = models.FileField(upload_to=get_zipped_data_path,
        null=True, blank=True, default=None, validators=[zipped_file_validator()])
    data_folder = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('base:project',
            kwargs=dict(project_slug=self.slug))

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.name))

        ports = {

        }

        ### This entire part might be best done asynchronously

        image_name_template = generate_docker_compose(self.slug)
        #run docker-compose up -p --no-recreate
        #for each of the image names, run docker port and get the host port
        project_app_ports = {}
        generate_nginx_config(self.slug, project_app_ports)
        #restart nginx

        #fill it in with each project's 

        if self.uploaded_data:
            super(Project, self).save(*args, **kwargs)
            unzip.delay(self.get_zipped_data_path(self.uploaded_data.name),
                    self.get_dumped_data_path())
            self.data_folder = self.get_dumped_data_path()

        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class App(models.Model):
    """
    Represents information about starting an application in a container.
    """
    name = models.CharField(max_length=64, unique=True,
        validators=[alphanumeric_validator()])
    index_url = models.URLField()

    #Only one of the following can be non-blank. This is not enforced yet.
    image = models.TextField(max_length=256, blank=True, null=True)
    build = models.TextField(max_length=265, blank=True, null=True)
    command = models.TextField(max_length=256)

    def create_container(self, project):
        pass



class AppLink(models.Model):
    from_app = models.ForeignKey(App)
    to_app = models.foreignkey(App)
    alias = models.TextField(App)

class AppPort(models.Model):
    app = models.ForeignKey(App, related_name=port_exposures)
    internal_port = models.IntegerField(null=False)
    service_name = models.TextField(max_length=64, null=True, blank=True)

    @property
    def internal_port(self):
        return self.app_port.internal_port

class VolumeMount(models.Model):
    """
    When creating this app, where to mount it in the container.

    TODO: More thinking required
    """
    app = models.ForeignKey(App)
    mounted_at = models.TextField(max_length=254)
    """Where within the container is it mounted?"""
    located_at = models.TextField(max_length=254)
    """Where on the host is the directory?"""
    read_only = models.BooleanField(default=False)

class EnvVar(modelx.Model):
    app = models.ForeignKey(App)
    name = models.TextField(max_length=64)
    value = modelx.TextField(max_length=256, default='')


class Container(models.Model):
    NGINX_CONFIG_TEMPLATE_PATH = os.path.join(settings.BASE_DIR, 'base/deploy_templates/nginx-reverse-proxy.conf.jinja2')
    DOCKER_COMPOSE_TEMPLATE_PATH = os.path.join(settings.BASE_DIR, 'base/deploy_templates/docker-compose.yml.jinja2')
    NGINX_CONFIG_DESTINATION_PATH = '/etc/nginx/sites-enabled/memex-reverse-proxy.conf'
    DOCKER_COMPOSE_DESTINATION_PATH = os.path.join(settings.BASE_DIR, 'base/docker-compose.yml')

    app = models.ForeignKey(App)
    project = models.ForeignKey(Project)
    "What type of app should the container be running?"
    high_port = models.IntegerField(null=True, blank=True)
    "If the app exposes a port, what high port does it end up exposing it on?"
    public_path_base = models.TextField(null=True, blank=True)
    "If the app is supposed to be served to the outside world and has a base url different than /project.name/app.name, what is it?"
    expose_publicly = models.BooleanField(default=False)
    "Should the app be exposed publicly?"
    running = models.BooleanField(default=False)
    "Should the container be running?"

    def slug(self):
        return "{}{}".format(self.project.name, self.app.name)

    def public_urlbase(self):
        if not self.expose_publicly:
            return None
        elif self.public_path_base:
            return self.public_path_base
        else:
            return "{}/{}".format(self.project.name, self.app.name)

    @classmethod
    def fill_template(cls, source, destination, context_dict):
        template = Template(open(source, 'r').read(), trim_blocks = True, lstrip_blocks = True)
        result = template.render(Context(**context_dict))
        with open(destination, 'w') as f:
            f.write(result)
            f.flush()

    @classmethod
    def generate_container_context(cls):
        containers = Container.objects.filter(running == True).select_related('app', 'project').all()
        return {'containers': containers}

    @classmethod
    def create_containers(cls):
        """
        Create a new docker compose file with an entry for every container that is supposed to be running.
        Then, restart nginx.
        """
        cls.fill_template(cls.DOCKER_COMPOSE_TEMPLATE_PATH, cls.DOCKER_COMPOSE_DESTINATION_PATH, cls.generate_container_context())

    @classmethod
    def generate_nginx_context(cls):
        containers = cls.objects.filter(expose_publicly == True).filter(running == True).select_related('app', 'project').all()
        root_port = os.environ.get('ROOT_PORT', '8000')
        hostname = os.environ.get('HOST_NAME', '')
        ip_addr = os.environ.get('IP_ADDR', '')
        return {'containers': containers, 'root_port': root_port, 'hostname': hostname, 'ip_addr': ip_addr}

    @classmethod
    def map_public_ports(cls):
        """
        Create a new nginx config with an entry for every container that is supposed to be running and has a public path base.
        Then, restart nginx.
        """
        cls.fill_template(cls.NGINX_CONFIG_TEMPLATE_PATH, cls.NGINX_CONFIG_DESTINATION_PATH, cls.generate_nginx_context())



class ContainerPort(models.Model):
    """
    After a container is created, for each of the ports that container exposes, we find what high port is exposed on and save it here.
    """
    container = models.ForeignKey(Container)
    app_port = models.ForeignKey(AppPort)
    external_port = models.IntegerField()
