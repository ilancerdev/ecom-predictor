# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-11 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walmart_api', '0002_submissionhistory_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionstatus',
            name='status',
            field=models.CharField(db_index=True, max_length=20),
        ),
    ]
