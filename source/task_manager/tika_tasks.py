"""
Test script for ingesting PDFs from the file system using Tika

Some code directly ripped from Katrina's autonomy work
"""

import json
import re
import os

from celery import shared_task, task

TIKA_ENDPOINT="http://0.0.0.0:9998"
ELASTICSEARCH_HOST="http://0.0.0.0:9200"

from elasticsearch import Elasticsearch
from tika.tika import parse1 as parse


from django.db import IntegrityError


from task_manager.models import CeleryTask


def process_content(content_str, stopwords):
    """Produces a nicer content string by removing stop words and numbers.
       Trying to also pull out keyword phrases for modeling in one pass."""
    cleaned = []
    features = {
        "pure teleoperation" : 0,
        "leader follower" : 0,
        "obstacle detection" : 0,
        "obstacle avoidance" : 0,
        "route planning" : 0,
        "mission planning" : 0,
        "target recognition" : 0,
        "autonomous mobility" : 0,
        "feature identification" : 0,
        "situational awareness" : 0,
        "collaborative systems" : 0,
        "adaptive behavior" : 0,
        "tactical behavior" : 0,
        }
    last_token = ''
    content_str = content_str.lower().split()
    for token in content_str:
        token = re.sub("[^a-zA-Z]", '', token)
        if not(token in stopwords):
            cleaned.append(token)
            keyword_phrase = last_token + ' ' + token
            if keyword_phrase in features.keys():
                features[keyword_phrase] = 1
            last_token = token
    content_str = " ".join(cleaned)
    return content_str, features


@shared_task(bind=True)
def create_index(self, index, *args, **kwargs):
    self.index = index
    # Check whether a CeleryTask already exists. If not, create the new object. If
    # yes (IntegrityError), update the rows of the already existing object.
    try:
        self.index_task = CeleryTask(index=self.index, uuid=self.request.id)
        self.index_task.save()
    except IntegrityError:
        self.index_task = CeleryTask.objects.get(index=self.index)
        self.index_task.uuid = self.request.id
        self.index_task.save()

    es = Elasticsearch([ELASTICSEARCH_HOST])
    files = [os.path.join(self.index.data_folder, x) for x in os.listdir(self.index.data_folder)]
    if es.indices.exists(self.index.slug):
        print("Deleting '%s' index" % self.index.slug)
        res = es.indices.delete(index=self.index.slug)
        print("  response: '%s'" % res)

    stopwords = []

    for f in files:
        #Using experimental tika library - just a little janky
        response = parse('all', f, TIKA_ENDPOINT)[1]
        try:
            if response[0] == '[':
                #Sometimes response comes in brackets
                parsed = json.loads(response[1:-1])
            else:
                #Sometimes not.
                parsed = json.loads(response)
            content, features = process_content(parsed["X-TIKA:content"], stopwords)
            parsed["X-TIKA:cleaned"] = content
            for kw, val in features.items():
                parsed["has_" + re.sub(' ', '_', kw)] = val
            #parsed["authors"] = process_authors(parsed["X-TIKA:content"])
            es.index(index="%s" % self.index.index_name,
                     doc_type="autonomy",
                     body = parsed,
                     )
        except Exception as e:
            #Strange errors coming from new tika parser
            #Just move on to the next document
            print e
            pass
