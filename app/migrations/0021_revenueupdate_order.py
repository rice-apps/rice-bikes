# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20150802_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='revenueupdate',
            name='order',
            field=models.ForeignKey(blank=True, to='app.PartOrder', null=True),
            preserve_default=True,
        ),
    ]
