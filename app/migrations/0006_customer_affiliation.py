# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20150207_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='affiliation',
            field=models.CharField(max_length=100, default=''),
            preserve_default=True,
        ),
    ]
