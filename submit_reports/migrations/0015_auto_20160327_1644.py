# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 16:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submit_reports', '0014_auto_20160327_0542'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='staff',
            name='courses',
            field=models.ManyToManyField(to='submit_reports.Course'),
        ),
        migrations.AddField(
            model_name='submitreport',
            name='service_type',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AddField(
            model_name='submitreport',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=8),
        ),
    ]
