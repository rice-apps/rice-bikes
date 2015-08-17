# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_revenueupdate_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partorder',
            name='name',
            field=models.CharField(default='Filler Name!', max_length=50),
            preserve_default=False,
        ),
    ]
