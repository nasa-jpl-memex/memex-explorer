# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crawl',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('crawler', models.CharField(max_length=64)),
                ('status', models.CharField(max_length=64)),
                ('config', models.CharField(max_length=64)),
                ('seeds_list', models.CharField(max_length=64)),
                ('pages_crawled', models.BigIntegerField()),
                ('harvest_rate', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('data_uri', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('crawl', models.ForeignKey(to='crawl_space.Crawl')),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='crawl',
            name='data_model',
            field=models.ForeignKey(to='crawl_space.DataModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crawl',
            name='project',
            field=models.ForeignKey(to='base.Project'),
            preserve_default=True,
        ),
    ]
