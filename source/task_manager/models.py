from django.db import models

from celery.result import AsyncResult

from apps.crawl_space.models import Crawl

from base.models import Index


class CeleryTask(models.Model):
    
    pid = models.IntegerField(default=0)
    crawl = models.OneToOneField(Crawl, blank=True, null=True, default=None)
    index = models.OneToOneField(Index, blank=True, null=True, default=None)
    uuid = models.TextField()

    @property
    def task(self):
        """
        Gives an instance of the crawl task which can be used to check on the
        status of the crawl.
        """
        return AsyncResult(self.uuid)

    def __unicode__(self):
        return str(self.uuid)
