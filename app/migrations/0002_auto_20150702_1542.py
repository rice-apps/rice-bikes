# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RevenueUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('employee', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('is_transaction', models.BooleanField(default=False)),
                ('completed_transaction', models.ForeignKey(to='app.Transaction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TotalRevenue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_revenue', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='refurbishedbike',
            name='vin',
            field=models.IntegerField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rentalbike',
            name='vin',
            field=models.IntegerField(unique=True),
            preserve_default=True,
        ),
    ]
