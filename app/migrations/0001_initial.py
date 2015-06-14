# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import app.models


class Migration(migrations.Migration):

    dependencies = [
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
                ('handlebars', models.CharField(blank=True, max_length=20, null=True, choices=[(b'2', b'COMPLETE'), (b'1', b'IN_PROGRESS'), (b'0', b'NOT_ASSIGNED')])),
                ('brakes', models.CharField(blank=True, max_length=20, null=True, choices=[(b'2', b'COMPLETE'), (b'1', b'IN_PROGRESS'), (b'0', b'NOT_ASSIGNED')])),
                ('frame', models.CharField(blank=True, max_length=20, null=True, choices=[(b'2', b'COMPLETE'), (b'1', b'IN_PROGRESS'), (b'0', b'NOT_ASSIGNED')])),
                ('completed', models.BooleanField(default=False)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
