# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 23:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_tracker', '0009_auto_20170905_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='records',
            name='deck',
            field=models.ManyToManyField(to='league_tracker.Decks'),
        ),
    ]
