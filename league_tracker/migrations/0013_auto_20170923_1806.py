# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-23 18:06
from __future__ import unicode_literals

from django.db import migrations

def add_bye(apps, schema_editor):
    User = apps.get_model('league_tracker', 'User')
    bye = User(user_id=1, name='BYE', is_bye=True)
    bye.save()
        
class Migration(migrations.Migration):

    dependencies = [
        ('league_tracker', '0012_auto_20170905_2334'),
    ]

    operations = [
        migrations.RunPython(add_bye)
    ]
