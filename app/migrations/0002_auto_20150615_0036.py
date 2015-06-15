# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='brakes',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'False', b'IN_PROGRESS'), (b'True', b'COMPLETE')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='frame',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'False', b'IN_PROGRESS'), (b'True', b'COMPLETE')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='handlebars',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'False', b'IN_PROGRESS'), (b'True', b'COMPLETE')]),
            preserve_default=True,
        ),
    ]
