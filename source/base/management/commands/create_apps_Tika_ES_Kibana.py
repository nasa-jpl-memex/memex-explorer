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
    image='dockerfile/elasticsearch'
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
    expose_publicly = True,
)
AppPort.objects.create(
    app = kibana,
    internal_port = 80
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
