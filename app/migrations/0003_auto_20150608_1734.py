# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150106_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('affiliation', models.CharField(default=b'', max_length=100)),
                ('email', models.CharField(max_length=100, validators=[app.models.validate_email])),
                ('service_description', models.CharField(max_length=500)),
                ('price', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('handlebars', models.CharField(default=b'', max_length=100)),
                ('brakes', models.CharField(default=b'', max_length=100)),
                ('frame', models.CharField(default=b'', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
