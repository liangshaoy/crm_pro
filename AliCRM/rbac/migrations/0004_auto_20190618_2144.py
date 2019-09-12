# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-18 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_auto_20190618_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission',
            options={'ordering': ['priority', 'id'], 'verbose_name': '权限表', 'verbose_name_plural': '权限表'},
        ),
        migrations.RemoveField(
            model_name='permission',
            name='menu',
        ),
        migrations.AddField(
            model_name='permission',
            name='priority',
            field=models.IntegerField(blank=True, help_text='菜单的显示顺序，优先级越小显示越靠前', null=True, verbose_name='显示优先级'),
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
    ]
