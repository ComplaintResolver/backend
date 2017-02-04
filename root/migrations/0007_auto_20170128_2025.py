# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-28 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0006_auto_20170128_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complainant',
            name='account_type',
            field=models.CharField(choices=[('twitter', 'twitter')], max_length=255),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(
                choices=[('waiting', 'waiting'), ('resolved', 'resolved'), ('rejected', 'rejected')], max_length=255),
        ),
    ]
