# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20150823_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='buybackbike',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='buybackbike',
            name='color',
            field=models.TextField(default='white'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buybackbike',
            name='model',
            field=models.TextField(default='Cannondale'),
            preserve_default=False,
        ),
    ]
