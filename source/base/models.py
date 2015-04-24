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
                'port': project_app_ports["{}{}".format(slug, app['name']),
            }
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
    name = models.CharField(max_length=64, unique=True,
        validators=[alphanumeric_validator()])
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    uploaded_data = models.FileField(upload_to=get_zipped_data_path,
        null=True, blank=True, default=None, validators=[zipped_file_validator()])
    data_folder = models.TextField(blank=True)

    def get_zipped_data_path(self, filename):
        return os.path.join(settings.PROJECT_PATH, self.slug, "zipped_data", filename)

    def get_dumped_data_path(self):
        return os.path.join(settings.PROJECT_PATH, self.slug, "data")

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
    

    """
    name = models.CharField(max_length=64, unique=True,
        validators=[alphanumeric_validator()])
    index_url = models.URLField()
