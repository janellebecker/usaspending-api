# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-28 14:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0070_mv_transaction_obligated_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialaccountsbyawardstransactionobligations',
            name='financial_accounts_by_awards',
        ),
        migrations.RemoveField(
            model_name='financialaccountsbyawardstransactionobligations',
            name='submission',
        ),
        migrations.DeleteModel(
            name='FinancialAccountsByAwardsTransactionObligations',
        ),
    ]
