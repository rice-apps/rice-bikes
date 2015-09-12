# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150908_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='refurbishedbike',
            name='sold',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
