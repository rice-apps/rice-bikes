# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150106_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('service_description', models.CharField(max_length=500)),
                ('price', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(to='app.Customer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='customer',
            name='price',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='service_description',
        ),
    ]
