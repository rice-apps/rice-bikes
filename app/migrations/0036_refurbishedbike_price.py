# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_refurbishedbike_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='refurbishedbike',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
