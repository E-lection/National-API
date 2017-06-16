# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('national', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConstituencyUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='PrivateKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
