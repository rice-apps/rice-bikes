# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_submitted',
            field=models.DateTimeField(verbose_name='date submitted'),
            preserve_default=True,
        ),
    ]
