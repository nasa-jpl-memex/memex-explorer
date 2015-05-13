from django.db import models

from apps.crawl_space.models import Crawl


class CrawlTask(models.Model):
    
    pid = models.IntegerField(default=0)
    crawl = models.ForeignKey(Crawl)
    uuid = models.TextField()
    returned = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.pid)

