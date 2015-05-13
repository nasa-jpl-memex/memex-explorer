from django.db import models

from celery.result import AsyncResult

from apps.crawl_space.models import Crawl


class CrawlTask(models.Model):
    
    pid = models.IntegerField(default=0)
    crawl = models.OneToOneField(Crawl)
    uuid = models.TextField()

    def get_task_status(self):
        return AsyncResult(self.uuid).status

    def __unicode__(self):
        return str(self.uuid)

