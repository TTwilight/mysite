# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-14 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profileuser_others'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='birth',
            field=models.DateField(blank=True, default='2017-01-01'),
        ),
    ]
