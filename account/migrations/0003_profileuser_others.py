# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-14 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170714_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileuser',
            name='others',
            field=models.TextField(default='SOME STRING'),
        ),
    ]