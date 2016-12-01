# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-01 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0043_auto_20161201_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialassistanceaward',
            name='submitted_type',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Submitted Type'),
        ),
        migrations.AlterField(
            model_name='financialassistanceaward',
            name='modification_number',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Modification Number'),
        ),
        migrations.AlterField(
            model_name='procurement',
            name='modification_number',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Modification Number'),
        ),
    ]