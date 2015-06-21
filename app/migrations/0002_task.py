# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('completed', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
                ('transaction', models.ForeignKey(to='app.Transaction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
