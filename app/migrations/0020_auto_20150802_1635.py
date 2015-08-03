# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20150728_2147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='task',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.RemoveField(
            model_name='task',
            name='name',
        ),
        migrations.AddField(
            model_name='task',
            name='menu_item',
            field=models.ForeignKey(default=None, to='app.MenuItem'),
            preserve_default=False,
        ),
    ]
