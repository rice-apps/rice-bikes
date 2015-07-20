# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20150718_1928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='price',
            new_name='cost',
        ),
        migrations.AlterField(
            model_name='partcategory',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'0', b'Headset'), (b'1', b'Bottom bracket'), (b'2', b'Frame and alignment'), (b'3', b'Brakes'), (b'4', b'Handlebars'), (b'5', b'Stem'), (b'6', b'Wheels'), (b'7', b'Shifters and derailleurs'), (b'8', b'Saddle and seatpost'), (b'9', b'Drive train')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='partcategory',
            name='price',
            field=models.IntegerField(default=b'0', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='affiliation',
            field=models.CharField(default=b'', max_length=100, choices=[(b'0', b'Undergraduate'), (b'1', b'Graduate'), (b'2', b'Faculty'), (b'3', b'Staff'), (b'4', b'Non-Affiliate'), (b'5', b'Employee')]),
            preserve_default=True,
        ),
    ]
