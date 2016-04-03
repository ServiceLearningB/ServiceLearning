# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 01:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit_reports', '0009_auto_20160327_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course',
            field=models.CharField(choices=[('CAMD', 'CAMD'), ('CCIS', 'CCIS'), ('COS', 'COS'), ('CSSH', 'CSSH'), ('BOUVE', 'BOUVE'), ('DMSB', 'DMSB'), ('COE', 'COE'), ('LAW', 'LAW'), ('CPS', 'CPS'), ('PROVOST', 'PROVOST'), ('NONE', 'NONE')], default='NONE', max_length=5),
        ),
    ]