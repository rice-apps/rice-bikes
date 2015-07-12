# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20150712_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revenueupdate',
            name='description',
        ),
    ]
