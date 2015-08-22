# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20150818_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False)),
                ('number', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccessoryMenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=b'0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuyBackBike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vin', models.IntegerField(unique=True)),
                ('color', models.TextField()),
                ('model', models.TextField()),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False)),
                ('number', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PartMenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=b'0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='MenuItem',
            new_name='TaskMenuItem',
        ),
        migrations.AddField(
            model_name='part',
            name='menu_item',
            field=models.ForeignKey(to='app.PartMenuItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='part',
            name='transaction',
            field=models.ForeignKey(to='app.Transaction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accessory',
            name='menu_item',
            field=models.ForeignKey(to='app.AccessoryMenuItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='accessory',
            name='transaction',
            field=models.ForeignKey(to='app.Transaction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='refurbishedbike',
            name='color',
            field=models.TextField(default='white'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='refurbishedbike',
            name='model',
            field=models.TextField(default='Cannondale'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
