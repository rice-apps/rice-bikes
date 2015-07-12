# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_transaction_amount_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='revenueupdate',
            old_name='completed_transaction',
            new_name='transaction',
        ),
    ]
