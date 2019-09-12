# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-18 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='menu_url',
            field=models.CharField(blank=True, help_text='是否给菜单设置一个url地址', max_length=300, null=True, verbose_name='菜单url地址'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(blank=True, help_text='是否给菜单设置一个url地址', max_length=300, null=True, verbose_name='权限url地址'),
        ),
    ]
