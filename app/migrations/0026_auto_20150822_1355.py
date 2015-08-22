# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20150822_1340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accessorymenuitem',
            options={'verbose_name': 'Menu Accessory Item', 'verbose_name_plural': 'Menu Accessory Items'},
        ),
    ]
