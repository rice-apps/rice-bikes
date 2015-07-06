# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_revenueupdate_new_total_revenue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revenueupdate',
            name='new_total_revenue',
            field=models.IntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='service_description',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
