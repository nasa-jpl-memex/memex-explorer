import sys
import os

from jinja2 import Template
from jinja2.runtime import Context

from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

# App
from base.forms import AddProjectForm
from base.models import (
    App,
    AppPort,
    VolumeMount,
    EnvVar,
    AppLink,

)

class Command(BaseCommand):
    help = 'Creates Tika, Elasticsearch, and Kibana apps'

    def handle(self, *args, **options):
        tika=App.objects.create(
            name='tika',
            image='continuumio/tika'
        )
        AppPort.objects.create(
            app = tika,
            internal_port = 9998
        )


        elasticsearch = App.objects.create(
            name='elasticsearch',
            image='elasticsearch'
        )
        AppPort.objects.create(
            app = elasticsearch,
            internal_port = 9200
        )
        AppPort.objects.create(
            app = elasticsearch,
            internal_port = 9300
        )
        VolumeMount.objects.create(
            app = elasticsearch,
            mounted_at = '/data',
            located_at = '/home/ubuntu/elasticsearch/data',
        )


        kibana = App.objects.create(
            name = 'kibana',
            image = 'continuumio/kibana',
        )
        AppPort.objects.create(
            app = kibana,
            internal_port = 80
            expose_publicly = True,
        )
        EnvVar.objects.create(
            app = kibana,
            name='KIBANA_SECURE',
            value='false'
        )
        AppLink.objects.create(
            from_app = kibana,
            to_app = elasticsearch,
            alias = 'es'
        )
