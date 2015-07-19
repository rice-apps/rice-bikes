# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_partcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partcategory',
            name='category',
            field=models.CharField(max_length=100, choices=[(0, b'Headset'), (1, b'Bottom bracket'), (2, b'Frame and alignment'), (3, b'Brakes'), (4, b'Handlebars'), (5, b'Stem'), (6, b'Wheels'), (7, b'Shifters and derailleurs'), (8, b'Saddle and seatpost'), (9, b'Drive train')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partcategory',
            name='transaction',
            field=models.ForeignKey(to='app.Transaction', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='affiliation',
            field=models.CharField(default=b'', max_length=100, choices=[(0, b'Undergraduate'), (1, b'Graduate'), (2, b'Faculty'), (3, b'Staff'), (4, b'Non-Affiliate'), (5, b'Employee')]),
            preserve_default=True,
        ),
    ]
