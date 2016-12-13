# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-13 14:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0009_auto_20161213_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='type',
            field=models.CharField(choices=[
                ('Personal Computer', 'Personal computer'),
                ('Monoblock', 'Monoblock'),
                ('Laptop', 'Laptop')],
                default='Personal Computer', max_length=30),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
