# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('ip_address', models.GenericIPAddressField(protocol='IPv4')),
                ('ipmi_ip_address', models.GenericIPAddressField(protocol='IPv4')),
                ('ipmi_user_name', models.CharField(max_length=200)),
                ('ipmi_password', models.CharField(max_length=200)),
            ],
        ),
    ]