# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-31 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_auto_20180318_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
    ]
