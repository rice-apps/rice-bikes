# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150615_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='brakes',
            field=models.CharField(default='NOT_ASSIGNED', max_length=1, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='frame',
            field=models.CharField(default='NOT_ASSIGNED', max_length=1, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='handlebars',
            field=models.CharField(default='NOT_ASSIGNED', max_length=1, blank=True),
            preserve_default=False,
        ),
    ]
