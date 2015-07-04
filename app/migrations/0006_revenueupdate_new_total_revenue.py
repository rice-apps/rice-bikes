# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_revenueupdate_date_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='revenueupdate',
            name='new_total_revenue',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
