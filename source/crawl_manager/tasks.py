from __future__ import absolute_import

import subprocess

from celery import shared_task, Task, uuid

from crawl_manager.models import CeleryTask


def db_register_task(pid):
    task = CeleryTask(pid=pid)
    task.save()
    return "success"


def repeat(uuid):
    print(uuid)


@shared_task()
def nutch(crawl, rounds, *args, **kwargs):
    call = ["crawl", crawl.seeds_list, crawl.get_crawl_path(), rounds]
    proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    db_register_task(proc.pid, crawl)
    stdout, stderr = proc.communicate()
    return "FINISHED"

@shared_task(bind=True)
def add(self, x, y):
    print(self.request.id)
    return x + y

