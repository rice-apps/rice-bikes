# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20150914_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='partmenuitem',
            name='price',
            field=models.IntegerField(default=b'0'),
            preserve_default=True,
        ),
    ]
