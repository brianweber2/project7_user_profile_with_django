# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 05:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=140),
        ),
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateTimeField(blank=True, default=''),
        ),
    ]
