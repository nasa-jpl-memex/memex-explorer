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
        tika=App.objects.get_or_create(
            name='tika',
            image='continuumio/tika'
        )[0]
        AppPort.objects.get_or_create(
            app = tika,
            internal_port = 9998
        )[0]


        elasticsearch = App.objects.get_or_create(
            name='elasticsearch',
            image='elasticsearch'
        )[0]
        AppPort.objects.get_or_create(
            app = elasticsearch,
            internal_port = 9200
        )[0]
        AppPort.objects.get_or_create(
            app = elasticsearch,
            internal_port = 9300
        )[0]
        VolumeMount.objects.get_or_create(
            app = elasticsearch,
            mounted_at = '/data',
            located_at = os.path.join(settings.BASE_DIR, 'container_volumes/elasticsearch/data'),
        )[0]


        kibana = App.objects.get_or_create(
            name = 'kibana',
            image = 'continuumio/kibana',
        )[0]
        AppPort.objects.get_or_create(
            app = kibana,
            internal_port = 80,
            expose_publicly = True,
        )[0]
        EnvVar.objects.get_or_create(
            app = kibana,
            name='KIBANA_SECURE',
            value='false'
        )[0]
        AppLink.objects.get_or_create(
            from_app = kibana,
            to_app = elasticsearch,
            alias = 'es'
        )[0]
