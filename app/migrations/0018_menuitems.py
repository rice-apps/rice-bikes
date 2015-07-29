# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_partcategory_date_submitted'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=b'0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
