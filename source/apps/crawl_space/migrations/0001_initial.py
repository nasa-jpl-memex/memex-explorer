# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.crawl_space.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crawl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, validators=[django.core.validators.RegexValidator(b'^[a-zA-Z0-9-_ ]+$', b'Only numbers, letters, underscores, dashes and spaces are allowed.')])),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('description', models.TextField(blank=True)),
                ('crawler', models.CharField(default=b'nutch', max_length=64, choices=[(b'nutch', b'Nutch'), (b'ache', b'ACHE')])),
                ('status', models.CharField(default=b'NOT STARTED', max_length=64)),
                ('config', models.CharField(default=b'config_default', max_length=64)),
                ('seeds_list', models.FileField(upload_to=apps.crawl_space.models.get_seeds_upload_path)),
                ('pages_crawled', models.BigIntegerField(default=0)),
                ('harvest_rate', models.FloatField(default=0)),
                ('location', models.CharField(default=b'location', max_length=64)),
                ('rounds_left', models.IntegerField(default=1, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CrawlModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(b'^[a-zA-Z0-9-_ ]+$', b'Only numbers, letters, underscores, dashes and spaces are allowed.')])),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('model', models.FileField(upload_to=apps.crawl_space.models.get_model_upload_path, validators=[apps.crawl_space.models.validate_model_file])),
                ('features', models.FileField(upload_to=apps.crawl_space.models.get_model_upload_path, validators=[apps.crawl_space.models.validate_features_file])),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='crawl',
            name='crawl_model',
            field=models.ForeignKey(default=None, blank=True, to='crawl_space.CrawlModel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crawl',
            name='project',
            field=models.ForeignKey(to='base.Project'),
            preserve_default=True,
        ),
    ]
