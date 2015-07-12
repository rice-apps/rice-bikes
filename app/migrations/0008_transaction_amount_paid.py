# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20150705_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount_paid',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
