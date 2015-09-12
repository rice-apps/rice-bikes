# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buybackbike',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='refurbishedbike',
            name='sold',
        ),
        migrations.RemoveField(
            model_name='refurbishedbike',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='rentalbike',
            name='transaction',
        ),
        migrations.AddField(
            model_name='transaction',
            name='buy_back_bike',
            field=models.ForeignKey(blank=True, to='app.BuyBackBike', null=True),
            preserve_default=True,
        ),
    ]
