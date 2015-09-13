# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_refurbishedbike_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_for_bike',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
