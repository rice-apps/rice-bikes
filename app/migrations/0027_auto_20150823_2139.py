# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20150822_1355'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buybackbike',
            options={'verbose_name': 'Bike Buy Back', 'verbose_name_plural': 'Bike Buy Backs'},
        ),
        migrations.AlterModelOptions(
            name='partmenuitem',
            options={'verbose_name': 'Menu Part Item', 'verbose_name_plural': 'Menu Part Items'},
        ),
        migrations.AlterModelOptions(
            name='refurbishedbike',
            options={'verbose_name': 'Bike Refurbished', 'verbose_name_plural': 'Bike Refurbished'},
        ),
        migrations.AlterModelOptions(
            name='rentalbike',
            options={'verbose_name': 'Bike Rental', 'verbose_name_plural': 'Bike Rentals'},
        ),
        migrations.AlterModelOptions(
            name='taskmenuitem',
            options={'verbose_name': 'Menu Task Item', 'verbose_name_plural': 'Menu Task Items'},
        ),
        migrations.AlterModelOptions(
            name='totalrevenue',
            options={'verbose_name': 'Total Revenue', 'verbose_name_plural': 'Total Revenue'},
        ),
        migrations.AddField(
            model_name='buybackbike',
            name='transaction',
            field=models.ForeignKey(blank=True, to='app.Transaction', null=True),
            preserve_default=True,
        ),
    ]
