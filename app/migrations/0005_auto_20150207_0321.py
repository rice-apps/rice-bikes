# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_auto_20150115_1704'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('type', models.CharField(max_length=500)),
                ('price', models.IntegerField(default=0)),
                ('fulfilled', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(to='app.Customer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='service',
            name='service_description',
        ),
        migrations.AddField(
            model_name='service',
            name='employee',
            field=models.ForeignKey(to='app.Employee', default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='service',
            name='fulfilled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='service',
            name='type',
            field=models.CharField(default='None', max_length=500),
            preserve_default=True,
        ),
    ]
