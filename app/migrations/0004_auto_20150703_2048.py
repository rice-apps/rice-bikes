# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_revenueupdate_is_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revenueupdate',
            name='completed_transaction',
            field=models.ForeignKey(blank=True, to='app.Transaction', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='revenueupdate',
            name='employee',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
