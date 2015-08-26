# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20150824_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessory',
            name='sold',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buybackbike',
            name='sold',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='part',
            name='sold',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='sold',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
