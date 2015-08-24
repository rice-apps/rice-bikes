# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20150823_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='buybackbike',
            name='completed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='buybackbike',
            name='color',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='buybackbike',
            name='model',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
