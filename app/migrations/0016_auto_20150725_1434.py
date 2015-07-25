# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20150723_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True, choices=[(b'0', b'Headset'), (b'1', b'Bottom bracket'), (b'2', b'Frame and alignment'), (b'3', b'Brakes'), (b'4', b'Handlebars'), (b'5', b'Stem'), (b'6', b'Wheels'), (b'7', b'Shifters and derailleurs'), (b'8', b'Saddle and seatpost'), (b'9', b'Drive train')])),
                ('was_ordered', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=b'0', null=True, blank=True)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Part',
        ),
    ]
