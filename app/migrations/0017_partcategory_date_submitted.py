# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20150725_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='partcategory',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
    ]
