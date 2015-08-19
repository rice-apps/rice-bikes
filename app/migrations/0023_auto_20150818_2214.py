# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20150816_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiscRevenueUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='revenueupdate',
            name='misc_revenue_update',
            field=models.ForeignKey(blank=True, to='app.MiscRevenueUpdate', null=True),
            preserve_default=True,
        ),
    ]
