# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-24 12:34
from __future__ import unicode_literals

import uuid

from django.db import migrations


def gen_uuid(apps, schema_editor):
    Catalogus = apps.get_model("datamodel", "Catalogus")
    ZaakType = apps.get_model("datamodel", "ZaakType")
    Eigenschap = apps.get_model("datamodel", "Eigenschap")
    StatusType = apps.get_model("datamodel", "StatusType")

    for Model in (Catalogus, ZaakType, Eigenschap, StatusType):
        for row in Model.objects.all():
            row.uuid = uuid.uuid4()
            row.save(update_fields=["uuid"])


class Migration(migrations.Migration):

    dependencies = [("datamodel", "0014_auto_20180724_1433")]

    operations = [migrations.RunPython(gen_uuid, migrations.RunPython.noop)]
