# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_partmenuitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='status',
            field=models.CharField(default=b'Available', max_length=50),
            preserve_default=True,
        ),
    ]
