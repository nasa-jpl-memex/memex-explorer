from __future__ import absolute_import

import subprocess
import os
import shlex
import time

from celery import shared_task, Task

from django.db import IntegrityError

from task_manager.models import CrawlTask

from apps.crawl_space.settings import LANG_DETECT_PATH
from apps.crawl_space.models import Crawl


def nutch_log_statistics(crawl):
    crawl_db_dir = os.path.join(crawl.get_crawl_path(), 'crawldb')
    stats_call = "nutch readdb {} -stats".format(crawl_db_dir)
    proc = subprocess.Popen(shlex.split(stats_call), stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    nutch_stats = stdout.decode()
    for line in stdout.split('\n'):
        if 'db_fetched' in line:
            crawl.pages_crawled = int(line.split('\t')[-1])
            crawl.save()


class NutchTask(Task):
    abstract = True

    def on_success(self, *args, **kwargs):
        nutch_log_statistics(self.crawl)
        self.crawl = Crawl.objects.get(pk=self.crawl.pk)
        self.crawl.status = self.crawl_task.task.status
        self.crawl.rounds_left -= 1
        self.crawl.save()
        if os.path.exists(os.path.join(self.crawl.get_crawl_path(), "stop")):
            os.remove(os.path.join(self.crawl.get_crawl_path(), "stop"))
            return
        if self.crawl.rounds_left >= 1:
            time.sleep(10)
            nutch.delay(self.crawl)


@shared_task(bind=True, base=NutchTask)
def nutch(self, crawl, rounds=1, *args, **kwargs):
    self.crawl = crawl
    call = [
        "crawl",
        crawl.seeds_list.path,
        crawl.get_crawl_path(),
        "1",
    ]
    with open(os.path.join(crawl.get_crawl_path(), 'crawl_proc.log'), 'a') as stdout:
        proc = subprocess.Popen(call, stdout=stdout, stderr=subprocess.PIPE,
            preexec_fn=os.setsid)
    try:
        self.crawl_task = CrawlTask(pid=proc.pid, crawl=self.crawl, uuid=self.request.id)
        self.crawl_task.save()
    except IntegrityError:
        self.crawl_task = CrawlTask.objects.get(crawl=self.crawl)
        self.crawl_task.pid = proc.pid
        self.crawl_task.uuid = self.request.id
        self.crawl_task.save()
    stdout, stderr = proc.communicate()
    return "Round Complete"


def ache_log_statistics(crawl):
    harvest_path = os.path.join(crawl.get_crawl_path(), 'data_monitor/harvestinfo.csv')
    proc = subprocess.Popen(["tail", "-n", "1", harvest_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if stderr and b"No such file or directory" not in stderr:
        raise AcheException(stderr)

    harvest_stats = stdout.decode()

    if not harvest_stats:
        return

    relevant, crawled = tuple(harvest_stats.split('\t')[:2])
    crawl.harvest_rate = "%.2f" % (float(relevant) / float(crawled))
    crawl.pages_crawled = crawled
    crawl.save()


@shared_task()
def ache(crawl, *args, **kwargs):
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
    return "Finished"

