import sys
import os

from jinja2 import Template
from jinja2.runtime import Context

from django.core.management.base import BaseCommand, CommandError
from base.models import Container

class Command(BaseCommand):
    help = 'Generate nginx config and restart nginx'

    def handle(self, *args, **options):
        Container.map_public_ports()
