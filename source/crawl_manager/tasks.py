from __future__ import absolute_import

import subprocess
import os

from celery import shared_task, Task

from crawl_manager.models import CeleryTask

from apps.crawl_space.settings import LANG_DETECT_PATH


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
    with open(os.path.join(crawl.get_crawl_path(), 'crawl_proc.log'), 'a') as stdout:
        proc = subprocess.Popen(call, stdout=stdout, stderr=subprocess.PIPE,
            preexec_fn=os.setsid)
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
        crawl.seeds_list.path,
        crawl.crawl_model.get_model_path(),
        LANG_DETECT_PATH,
    ]
    with open(os.path.join(crawl.get_crawl_path(), 'crawl_proc.log'), 'a') as stdout:
        proc = subprocess.Popen(call, stdout=stdout, stderr=subprocess.PIPE,
            preexec_fn=os.setsid)
    task = CeleryTask(pid=proc.pid, crawl=crawl, uuid=self.request.id)
    task.save()
    stdout, stderr = proc.communicate()
    return "FINISHED"

