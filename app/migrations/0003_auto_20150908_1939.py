# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150901_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buybackbike',
            name='color',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='buybackbike',
            name='model',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='refurbishedbike',
            name='color',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='refurbishedbike',
            name='model',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
