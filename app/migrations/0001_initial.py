# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, validators=[app.models.validate_email])),
                ('service_description', models.CharField(max_length=500)),
                ('price', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('date_submitted', models.DateTimeField(verbose_name=b'date submitted')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
