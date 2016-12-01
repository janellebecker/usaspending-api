# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 21:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0040_auto_20161107_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='financial_accounts_by_awards',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='awards.FinancialAccountsByAwards'),
        ),
        migrations.AlterField(
            model_name='award',
            name='type',
            field=models.CharField(choices=[('2', 'Block Grant'), ('3', 'Formula Grant'), ('4', 'Project Grant'), ('5', 'Cooperative Agreement'), ('6', 'Direct Payment for Specified Use'), ('7', 'Direct Loan'), ('8', 'Guaranteed/Insured Loan'), ('9', 'Insurance'), ('10', 'Direct Payment unrestricted'), ('11', 'Other')], max_length=5, verbose_name='Award Type'),
        ),
    ]