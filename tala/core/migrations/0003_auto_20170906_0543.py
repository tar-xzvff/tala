# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170906_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metrics',
            name='created_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
