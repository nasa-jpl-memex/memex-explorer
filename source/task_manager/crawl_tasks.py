from __future__ import absolute_import

import json
import subprocess
import os
import sys
import time
from celery import shared_task, Task
from apps.crawl_space.models import Crawl

from django.db import IntegrityError

from task_manager.models import CeleryTask
import nutch as nutch_rest_api
from apps.crawl_space.viz.stream import NutchUrlTrails

from django.conf import settings

ENABLE_STREAM_VIZ = settings.ENABLE_STREAM_VIZ
STREAM_UPDATE_PERIOD = 0.1

nutch_path = 'nutch'
crawl_path = 'crawl'
ache_path = 'ache'


def cca_dump(crawl):
    # TODO - check if this is necessary, for now assuming I need same
    # config to correctly dump a given crawl
    if ENABLE_STREAM_VIZ:
        config_name = 'config_streaming_' + self.crawl.name
        nutch_client = nutch_rest_api.Nutch(confId=config_name)
    else:
        nutch_client = nutch_rest_api.Nutch()

    job_client = nutch_client.Jobs(crawl.name)
    job_client.commoncrawldump()

# TODO - refactor below, these methods are getting a bit big

class NutchTask(Task):
    abstract = True

@shared_task(bind=True, base=NutchTask)
def nutch(self, crawl, rounds=1, *args, **kwargs):
    self.crawl = crawl
    self.crawl_task = None

    if ENABLE_STREAM_VIZ:
        # need to reconfigure nutch
        config_client = nutch_rest_api.Nutch().Configs()

        streaming_overrides = {'fetcher.publisher':'true',
                               'publisher.queue.type': 'rabbitmq',
                               'rabbitmq.exchange.type': 'direct',
                               'rabbitmq.queue.routingkey': self.crawl.name}

        config_name = 'config_streaming_' + self.crawl.name
        config_client[config_name] = streaming_overrides

        nutch_client = nutch_rest_api.Nutch(confId=config_name)
        url_trails = NutchUrlTrails(self.crawl.name)
    else:
        nutch_client = nutch_rest_api.Nutch()
        url_trails = None

    seed_client = nutch_client.Seeds()

    seed_urls = json.loads(self.crawl.seeds_object.seeds)
    seed = seed_client.create(self.crawl.slug + '_seed', seed_urls)

    job_client = nutch_client.Jobs(self.crawl.name)

    rest_crawl = nutch_client.Crawl(seed, jobClient=job_client, rounds=self.crawl.rounds_left)
    nutch_crawl(self.crawl, rest_crawl, url_trails)


def nutch_crawl(crawl_model, rest_crawl, url_trails):
    """
    Run a Nutch crawl until self.rounds_left is 0 or self.crawl.status is externally set to "STOPPING"

    :param crawl_model: The crawl model
    :param rest_crawl: A NutchPy Crawl Client
    :param url_trails: A UrlTrails object for visualizing streaming messages from Nutch
    """

    while crawl_model.rounds_left:
        if rest_crawl.currentJob is None:
            rest_crawl.currentJob = rest_crawl.jobClient.create('GENERATE')

        active_job = rest_crawl.progress(nextRound=False)
        while active_job:
            crawl_model = Crawl.objects.get(id=crawl_model.id)
            sys.stderr.write("Crawler Status: {}".format(crawl_model.status))
            if crawl_model.status == 'STOPPING':
                crawl_model.status = 'STOPPED'
                crawl_model.save()
                return
            time.sleep(STREAM_UPDATE_PERIOD)
            old_job = active_job
            active_job = rest_crawl.progress(nextRound=False)
            if url_trails:
                url_trails.handle_messages()
            if active_job and active_job != old_job:
                crawl_model.status = active_job.info()['type']
                crawl_model.save()
        crawl_model.rounds_left -= 1
        try:
            stats = rest_crawl.jobClient.stats()
        except nutch_rest_api.NutchException as err:
            sys.stderr.write(str(err))
        else:
            for ignore, data in stats['status'].items():
                if data['statusValue'] == 'db_fetched':
                    crawl_model.pages_crawled = data['count']
                    break
            else:
                sys.stderr.write("Warning: Nutch has responded but has not crawled anything yet")
        crawl_model.save()
    crawl_model.status = 'SUCCESS'
    crawl_model.save()
    

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


@shared_task(bind=True)
def ache(self, crawl, *args, **kwargs):
    self.crawl = crawl
    call = [
        ache_path,
        "startCrawl",
        "-o",
        self.crawl.get_crawl_path(),
        "-c",
        self.crawl.get_config_path(),
        "-s",
        self.crawl.seeds_list.path,
        "-m",
        self.crawl.crawl_model.get_model_path(),
        "-e",
        self.crawl.index_name,
    ]
    with open(os.path.join(self.crawl.get_crawl_path(), 'crawl_proc.log'), 'a') as stdout:
        proc = subprocess.Popen(call, stdout=stdout, stderr=subprocess.PIPE,
            preexec_fn=os.setsid)

    # Check whether a CeleryTask already exists. If no, create the new object. If
    # yes (IntegrityError), update the rows of the already existing object.
    try:
        self.crawl_task = CeleryTask(pid=proc.pid, crawl=self.crawl, uuid=self.request.id)
        self.crawl_task.save()
    except IntegrityError:
        self.crawl_task = CeleryTask.objects.get(crawl=self.crawl)
        self.crawl_task.pid = proc.pid
        self.crawl_task.uuid = self.request.id
        self.crawl_task.save()
    stdout, stderr = proc.communicate()
    if proc.returncode > 0:
        raise RuntimeError("Crawl has failed. Please review the crawl logs.")
    return "Stopped"
