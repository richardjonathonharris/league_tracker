# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_tracker', '0003_records_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='corp_status',
            field=models.CharField(choices=[('WI', 'Win'), ('TW', 'Timed Win'), ('TL', 'Timed Loss'), ('LO', 'Lose'), ('TI', 'Tie')], default='WI', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='records',
            name='round_num',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15)], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='records',
            name='runner_status',
            field=models.CharField(choices=[('WI', 'Win'), ('TW', 'Timed Win'), ('TL', 'Timed Loss'), ('LO', 'Lose'), ('TI', 'Tie')], default='WI', max_length=2, null=True),
        ),
    ]