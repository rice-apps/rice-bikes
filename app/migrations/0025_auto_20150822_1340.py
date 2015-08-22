# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20150822_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partmenuitem',
            name='price',
        ),
        migrations.AddField(
            model_name='part',
            name='price',
            field=models.IntegerField(default=b'0'),
            preserve_default=True,
        ),
    ]
