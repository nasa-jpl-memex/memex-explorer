from celery import shared_task
from base.models import Project
from base.models import App 
from base.models import Container

@shared_task()
def start_containers(project, app_names = ['tika', 'elasticsearch', 'kibana'], **kwargs):
    containers = []
    for app in App.objects.filter(name__in = app_names).all():
        containers.append(app.create_container_entry(project))
    Container.create_containers()
    Container.map_public_ports()
