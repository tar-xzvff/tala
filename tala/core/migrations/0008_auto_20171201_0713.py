# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-01 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_virtualmachine_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='password',
            field=models.CharField(blank=True, max_length=200, verbose_name='管理ユーザパスワード'),
        ),
        migrations.AlterField(
            model_name='virtualmachine',
            name='allocate_memory',
            field=models.CharField(blank=True, choices=[('512', '512MB'), ('1024', '1GB'), ('2048', '2GB'), ('4096', '4GB')], max_length=200, verbose_name='割り当てメモリ容量'),
        ),
    ]