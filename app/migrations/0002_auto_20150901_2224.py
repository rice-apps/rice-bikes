# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='refurbishedbike',
            name='transaction',
            field=models.ForeignKey(to='app.Transaction', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rentalbike',
            name='transaction',
            field=models.ForeignKey(to='app.Transaction', null=True),
            preserve_default=True,
        ),
    ]
