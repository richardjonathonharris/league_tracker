# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_tracker', '0002_auto_20170829_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='records',
            name='display',
            field=models.BooleanField(default=True),
        ),
    ]
