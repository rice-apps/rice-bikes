# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20150712_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
                ('transaction', models.ForeignKey(to='app.Transaction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
