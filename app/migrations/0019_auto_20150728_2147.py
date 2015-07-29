# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_menuitems'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MenuItems',
            new_name='MenuItem',
        ),
    ]
