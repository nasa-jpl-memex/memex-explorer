from django.db import models

from apps.crawl_space.models import Crawl


class CeleryTask(models.Model):
    
    pid = models.IntegerField(default=0)
    crawl = models.ForeignKey(Crawl)
    uuid = models.TextField()

    def __unicode__(self):
        return self.pid

