# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0034_auto_20161013_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialassistanceaward',
            name='cfda_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
