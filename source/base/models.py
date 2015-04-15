"""Base models."""

from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse

from jinja2 import Template
from jinja2.runtime import Context


def alphanumeric_validator():
    return RegexValidator(r'^[a-zA-Z0-9-_ ]+$',
        'Only numbers, letters, underscores, dashes and spaces are allowed.')


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

    def get_absolute_url(self):
        return reverse('base:project',
            kwargs=dict(project_slug=self.slug))

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.name))
        ports = {

        }
        APPS = [
            {
                'name': 'web',
                'dockerfile' : ".",
                'command' : "python ./manage.py runserver 0.0.0.0:8000",
                'volumes': [("./source", "./source")],
                'expose' : [8000],
            }, {
                'name': 'solr',
                'dockerfile' : "/home/ubuntu/solr_docker",
                'command' : "/home/ubuntu/solr_docker/solr_entry.sh",
                'volumes': [("/home/ubuntu/solr_docker", "/workdir")],
                'expose': [8983, 5005,]
            }
        ]
        context = {
            'hostname' : 'structureandinterperetation.com',
            'root_port' : 8617,
            'projects' : list(Project.objects.values('slug')) + [{'slug': self.slug}],
            'apps' : APPS
        }
        nginx_template = Template(open('/home/ubuntu/memex-explorer/deploy/nginx-reverse-proxy.conf.jinja2', 'r').read(),
                                    trim_blocks = True, lstrip_blocks = True)
        nginx_config = nginx_template.render(**context)
        with open('/home/ubuntu/memex-explorer/nginx-reverse-proxy.conf', 'w') as f:
            f.write(nginx_config)
            f.flush()
        compose_template = Template(open('/home/ubuntu/memex-explorer/deploy/docker-compose.yml.jinja2', 'r').read(),
                                    trim_blocks = True, lstrip_blocks = True)
        compose_config = compose_template.render(trim_blocks = True, lstrip_blocks = True, **context)
        with open('/home/ubuntu/memex-explorer/docker-compose.yml', 'w') as f:
            f.write(compose_config)
            f.flush()

        #fill it in with each project's 
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class App(models.Model):
    """
    

    """
    name = models.CharField(max_length=64, unique=True,
        validators=[alphanumeric_validator()])
    index_url = models.URLField()
