from django.db import models

from django.utils.text import slugify


class Project(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so save to get self.id
            super(Project, self).save(*args, **kwargs)
        self.slug = '%i-%s' % (
            self.id, slugify(self.name)
        )
        super(Project, self).save(*args, **kwargs)


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

