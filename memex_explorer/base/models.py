"""Base models."""

from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator


def alphanumeric_validator():
    return RegexValidator(r'^[a-zA-Z0-9 ]+$',
        'Only numbers, letters, and spaces are allowed.')


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
    description = models.TextField()

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('base:project',
            kwargs=dict(slug=self.slug))
