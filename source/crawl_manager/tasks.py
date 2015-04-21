from __future__ import absolute_import

import subprocess

from celery import shared_task

from crawl_manager.models import CeleryTask


class NutchTask(Task):
    abstract = True


@shared_task(bind=True, base=NutchTask)
def nutch(self, crawl, rounds, *args, **kwargs):
    call = [
        "crawl",
        crawl.seeds_list.path,
        crawl.get_crawl_path(),
        rounds,
    ]
    proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    task = CeleryTask(pid=proc.pid, crawl=crawl, uuid=self.request.id)
    task.save()
    stdout, stderr = proc.communicate()
    return "FINISHED"


class AcheTask(Task):
    abstract = True


@shared_task(bind=True, base=AcheTask)
def ache(self, crawl, *args, **kwargs):
    call = [
        "ache",
        "startCrawl",
        crawl.get_crawl_path(),
        crawl.get_config_path(),
        crawl.crawl_model.get_model_path(),
    ]
    proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    task = CeleryTask(pid=proc.pid, crawl=crawl, uuid=self.request.id)
    task.save()
    stdout, stderr = proc.communicate()
    return "FINISHED"

