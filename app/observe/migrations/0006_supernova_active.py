# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observe', '0005_auto_20161214_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='supernova',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
