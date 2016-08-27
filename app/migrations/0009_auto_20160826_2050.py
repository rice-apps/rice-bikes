# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_part_date_submitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='status',
            field=models.CharField(default=b'Available', max_length=50, choices=[(b'Avail', b'Available'), (b'Out', b'Out of Stock'), (b'Ordered', b'Ordered')]),
        ),
    ]
