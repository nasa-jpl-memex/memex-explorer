# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='uploaded_data',
            field=models.FileField(default=None, validators=[django.core.validators.RegexValidator(b'.*\\.(ZIP|zip)$', b'Only compressed archive (.zip) files are allowed.')], upload_to=base.models.get_zipped_data_path, blank=True, null=True),
            preserve_default=True,
        ),
    ]
