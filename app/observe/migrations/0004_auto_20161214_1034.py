# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 10:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observe', '0003_auto_20161214_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exposure',
            name='filter_name',
            field=models.CharField(choices=[('Ha', 'H-alpha'), ('D51', 'D51'), ('H-Beta', 'H Beta'), ('OIII', 'OIII'), ('H-Alpha', 'H Alpha'), ('Skymapper-VS', 'Skymapper CaV'), ('solar', 'Solar (V+R)'), ('Astrodon-UV', 'Astrodon UV'), ('I', 'Bessell-I'), ('R', 'Bessell-R'), ('U', 'Bessell-U'), ('w', 'PanSTARRS-w'), ('Y', 'PanSTARRS-Y'), ('up', 'SDSS-u&prime;'), ('air', 'Clear'), ('rp', 'SDSS-r&prime;'), ('ip', 'SDSS-i&prime;'), ('gp', 'SDSS-g&prime;'), ('zs', 'PanSTARRS-Z'), ('V', 'Bessell-V'), ('B', 'Bessell-B'), ('clear', 'clear')], max_length=30),
        ),
    ]
