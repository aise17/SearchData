# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 08:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webInfo', '0002_auto_20170725_1034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='passwoerd',
            new_name='password',
        ),
    ]