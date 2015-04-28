
from django.core.management.base import BaseCommand, CommandError
from base.models import * #this command is a throwaway.

class Command(BaseCommand):
    def handle(*args, **kwargs):
        Container.create_containers()
        print Container.generate_nginx_context()
        print Container.map_public_ports()
        print(open(Container.NGINX_CONFIG_DESTINATION_PATH, 'r').read())

