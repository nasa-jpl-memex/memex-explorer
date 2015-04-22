"""Base models."""

import os

from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse

from django.conf import settings

from task_manager.file_tasks import unzip


def alphanumeric_validator():
    return RegexValidator(r'^[a-zA-Z0-9-_ ]+$',
        'Only numbers, letters, underscores, dashes and spaces are allowed.')

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
        unzip.delay(self.uploaded_data.file, self.get_dumped_data_path())
        self.data_folder = self.get_dumped_data_path()
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

