# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_transaction_is_for_bike'),
    ]

    operations = [
        migrations.AddField(
            model_name='refurbishedbike',
            name='completed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
