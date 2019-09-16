# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-17 13:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("datamodel", "0007_auto_20180517_1544")]

    operations = [
        migrations.RenameField(
            model_name="besluittype",
            old_name="datum_begin_geldigheid_new",
            new_name="datum_begin_geldigheid",
        ),
        migrations.RenameField(
            model_name="besluittype",
            old_name="datum_einde_geldigheid_new",
            new_name="datum_einde_geldigheid",
        ),
        migrations.RenameField(
            model_name="eigenschap",
            old_name="datum_begin_geldigheid_new",
            new_name="datum_begin_geldigheid",
        ),
        migrations.RenameField(
            model_name="eigenschap",
            old_name="datum_einde_geldigheid_new",
            new_name="datum_einde_geldigheid",
        ),
        migrations.RenameField(
            model_name="informatieobjecttype",
            old_name="datum_begin_geldigheid_new",
            new_name="datum_begin_geldigheid",
        ),
        migrations.RenameField(
            model_name="informatieobjecttype",
            old_name="datum_einde_geldigheid_new",
            new_name="datum_einde_geldigheid",
        ),
        migrations.RenameField(
            model_name="informatieobjecttypeomschrijvinggeneriek",
            old_name="datum_begin_geldigheid_new",
            new_name="datum_begin_geldigheid",
        ),
        migrations.RenameField(
            model_name="informatieobjecttypeomschrijvinggeneriek",
            old_name="datum_einde_geldigheid_new",
            new_name="datum_einde_geldigheid",
        ),
        migrations.RenameField(
            model_name="resultaattype",
            old_name="datum_begin_geldigheid_new",
            new_name="datum_begin_geldigheid",
        ),
        migrations.RenameField(
            model_name="resultaattype",
            old_name="datum_einde_geldigheid_new",
            new_name="datum_einde_geldigheid",
        ),
        migrations.RenameField(
            model_name="roltype",
            old_name="datum_begin_geldigheid_new",
            new_name="datum_begin_geldigheid",
        ),
        migrations.RenameField(
            model_name="roltype",
            old_name="datum_einde_geldigheid_new",
            new_name="datum_einde_geldigheid",
        ),
        migrations.RenameField(
            model_name="statustype",
            old_name="datum_begin_geldigheid_new",
            new_name="datum_begin_geldigheid",
        ),
        migrations.RenameField(
            model_name="statustype",
            old_name="datum_einde_geldigheid_new",
            new_name="datum_einde_geldigheid",
        ),
        migrations.RenameField(
            model_name="zaakobjecttype",
            old_name="datum_begin_geldigheid_new",
            new_name="datum_begin_geldigheid",
        ),
        migrations.RenameField(
            model_name="zaakobjecttype",
            old_name="datum_einde_geldigheid_new",
            new_name="datum_einde_geldigheid",
        ),
        migrations.RenameField(
            model_name="zaaktype",
            old_name="datum_begin_geldigheid_new",
            new_name="datum_begin_geldigheid",
        ),
        migrations.RenameField(
            model_name="zaaktype",
            old_name="datum_einde_geldigheid_new",
            new_name="datum_einde_geldigheid",
        ),
        migrations.RenameField(
            model_name="zaaktype", old_name="versiedatum_new", new_name="versiedatum"
        ),
    ]
