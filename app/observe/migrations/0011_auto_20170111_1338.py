# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 13:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observe', '0010_auto_20170110_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supernova',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]