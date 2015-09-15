# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150913_2141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='service_description',
            new_name='bike_description',
        ),
    ]
