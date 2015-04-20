from __future__ import absolute_import

import subprocess

from celery import shared_task

from crawl_manager.models import CeleryTask


def db_register_task(pid):
    task = CeleryTask(pid=pid)
    task.save()


@shared_task()
def nutch(seed_dir, crawl_dir, rounds, *args, **kwargs):
    call = ["crawl", seed_dir, crawl_dir, rounds]
    proc = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    db_register_task(proc.pid)
    stdout, stderr = proc.communicate()
    return "FINISHED"

