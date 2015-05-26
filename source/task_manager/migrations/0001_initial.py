# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawl_space', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pid', models.IntegerField(default=0)),
                ('uuid', models.TextField()),
                ('crawl', models.OneToOneField(to='crawl_space.Crawl')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
