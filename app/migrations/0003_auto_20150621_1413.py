# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='brakes',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='frame',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='handlebars',
        ),
    ]
