# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-17 15:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_auto_20180118_2206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['area']},
        ),
        migrations.RenameField(
            model_name='card',
            old_name='_area',
            new_name='area',
        ),
    ]