# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0005_auto_20161211_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='price',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='quantity',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='type',
            field=models.CharField(
                choices=[
                    ('Personal Computer', 'Personal computer'),
                    ('Laptop', 'Laptop'),
                    ('Monoblock', 'Monoblock')],
                default='Personal Computer',
                max_length=30),
        ),
    ]