# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-13 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0021_mogelijkebetrokkene'),
    ]

    operations = [
        migrations.AddField(
            model_name='mogelijkebetrokkene',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='roltype',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
