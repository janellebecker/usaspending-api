# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-13 05:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0065_merge_20170213_2037'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='transaction',
            index_together=set([('award', 'action_date')]),
        ),
    ]
