# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20151127_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partcategory',
            name='transaction',
        ),
        migrations.DeleteModel(
            name='PartCategory',
        ),
        migrations.RemoveField(
            model_name='revenueupdate',
            name='order',
        ),
        migrations.DeleteModel(
            name='PartOrder',
        ),
    ]
