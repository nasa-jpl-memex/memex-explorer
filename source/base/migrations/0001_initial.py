# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, validators=[django.core.validators.RegexValidator(b'^[a-zA-Z0-9-_ ]+$', b'Only numbers, letters, underscores, dashes and spaces are allowed.')])),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('uploaded_data', models.FileField(upload_to=base.models.get_zipped_data_path, validators=[django.core.validators.RegexValidator(b'.*\\.(ZIP|zip)$', b'Only compressed archive (.zip) files are allowed.')])),
                ('data_folder', models.TextField(blank=True)),
                ('status', models.CharField(default=b'', max_length=64)),
                ('num_files', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, validators=[django.core.validators.RegexValidator(b'^[a-zA-Z0-9-_ ]+$', b'Only numbers, letters, underscores, dashes and spaces are allowed.')])),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('description', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeedsList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, validators=[django.core.validators.RegexValidator(b'^[a-zA-Z0-9-_ ]+$', b'Only numbers, letters, underscores, dashes and spaces are allowed.')])),
                ('seeds', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='index',
            name='project',
            field=models.ForeignKey(to='base.Project'),
            preserve_default=True,
        ),
    ]
