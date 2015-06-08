# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('crawl_space', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pid', models.IntegerField(default=0)),
                ('uuid', models.TextField()),
                ('crawl', models.OneToOneField(null=True, default=None, blank=True, to='crawl_space.Crawl')),
                ('index', models.OneToOneField(null=True, default=None, blank=True, to='base.Index')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
