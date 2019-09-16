# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-15 09:32
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [("datamodel", "0024_auto_20180813_1213")]

    operations = [
        migrations.AddField(
            model_name="informatieobjecttype",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                help_text="Unieke resource identifier (UUID4)",
                unique=True,
            ),
        )
    ]
