# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import app.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False)),
                ('number', models.IntegerField()),
                ('sold', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=b'0')),
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
                'verbose_name': 'Menu Accessory Item',
                'verbose_name_plural': 'Menu Accessory Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuyBackBike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vin', models.IntegerField(unique=True)),
                ('completed', models.BooleanField(default=False)),
                ('color', models.TextField(null=True, blank=True)),
                ('model', models.TextField(null=True, blank=True)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('price', models.IntegerField(default=0)),
                ('sold', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Bike Buy Back',
                'verbose_name_plural': 'Bike Buy Backs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False)),
                ('number', models.IntegerField()),
                ('price', models.IntegerField(default=b'0')),
                ('sold', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PartCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True, choices=[(b'0', b'Headset'), (b'1', b'Bottom bracket'), (b'2', b'Frame and alignment'), (b'3', b'Brakes'), (b'4', b'Handlebars'), (b'5', b'Stem'), (b'6', b'Wheels'), (b'7', b'Shifters and derailleurs'), (b'8', b'Saddle and seatpost'), (b'9', b'Drive train')])),
                ('price', models.IntegerField(default=b'0', null=True, blank=True)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
                ('was_used', models.BooleanField(default=False)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
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
            ],
            options={
                'verbose_name': 'Menu Part Item',
                'verbose_name_plural': 'Menu Part Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PartOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
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
        migrations.CreateModel(
            name='RefurbishedBike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vin', models.IntegerField(unique=True)),
                ('color', models.TextField(null=True, blank=True)),
                ('model', models.TextField(null=True, blank=True)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('sold', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Bike Refurbished',
                'verbose_name_plural': 'Bike Refurbished',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RentalBike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vin', models.IntegerField(unique=True)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
            options={
                'verbose_name': 'Bike Rental',
                'verbose_name_plural': 'Bike Rentals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RevenueUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('employee', models.CharField(max_length=100, blank=True)),
                ('new_total_revenue', models.IntegerField(blank=True)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('misc_revenue_update', models.ForeignKey(blank=True, to='app.MiscRevenueUpdate', null=True)),
                ('order', models.ForeignKey(blank=True, to='app.PartOrder', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.BooleanField(default=False)),
                ('number', models.IntegerField()),
                ('sold', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=b'0')),
                ('is_front', models.NullBooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskMenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=b'0')),
            ],
            options={
                'verbose_name': 'Menu Task Item',
                'verbose_name_plural': 'Menu Task Items',
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
                'verbose_name': 'Total Revenue',
                'verbose_name_plural': 'Total Revenue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('affiliation', models.CharField(default=b'', max_length=100, choices=[(b'0', b'Undergraduate'), (b'1', b'Graduate'), (b'2', b'Faculty'), (b'3', b'Staff'), (b'4', b'Non-Affiliate'), (b'5', b'Employee')])),
                ('email', models.CharField(max_length=100, validators=[app.models.validate_email])),
                ('service_description', models.CharField(max_length=500, null=True, blank=True)),
                ('cost', models.IntegerField(default=0)),
                ('amount_paid', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('is_for_bike', models.BooleanField(default=False)),
                ('buy_back_bike', models.ForeignKey(blank=True, to='app.BuyBackBike', null=True)),
                ('refurbished_bike', models.ForeignKey(blank=True, to='app.RefurbishedBike', null=True)),
                ('rental_bike', models.ForeignKey(blank=True, to='app.RentalBike', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='menu_item',
            field=models.ForeignKey(to='app.TaskMenuItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='transaction',
            field=models.ForeignKey(to='app.Transaction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='revenueupdate',
            name='transaction',
            field=models.ForeignKey(blank=True, to='app.Transaction', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partcategory',
            name='transaction',
            field=models.ForeignKey(to='app.Transaction', blank=True),
            preserve_default=True,
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
    ]
