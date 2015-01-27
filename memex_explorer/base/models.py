from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator


def alphanumeric_validator():
    return RegexValidator(r'^[a-zA-Z0-9 ]+$',
        'Only alphanumeric characters are allowed.')


class Project(models.Model):
    name = models.CharField(max_length=64, validators=[alphanumeric_validator()])
    slug = models.SlugField(max_length=64)
    description = models.TextField()
    icon = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class DataModel(models.Model):
    name = models.CharField(max_length=64)
    project = models.ForeignKey(Project)

    def __str__(self):
        return self.name


class Crawl(models.Model):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=64)
    description = models.TextField()
    crawler = models.CharField(max_length=64)
    status = models.CharField(max_length=64)
    config = models.CharField(max_length=64)
    seeds_list = models.CharField(max_length=64)
    pages_crawled = models.BigIntegerField()
    harvest_rate = models.FloatField()
    project = models.ForeignKey(Project)
    data_model = models.ForeignKey(DataModel)

    def __str__(self):
        return self.name


class DataSource(models.Model):
    name = models.CharField(max_length=64)
    data_uri = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project)
    crawl = models.ForeignKey(Crawl)

    def __str__(self):
        return self.name

