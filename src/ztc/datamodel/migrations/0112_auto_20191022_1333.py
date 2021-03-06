# Generated by Django 2.2.4 on 2019-10-22 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("datamodel", "0111_auto_20190924_1547")]

    operations = [
        migrations.RenameField(
            model_name="besluittype",
            old_name="informatieobjecttypes",
            new_name="informatieobjecttypen",
        ),
        migrations.AlterField(
            model_name="informatieobjecttype",
            name="zaaktypes",
            field=models.ManyToManyField(
                help_text="ZAAKTYPE met ZAAKen die relevant kunnen zijn voor dit INFORMATIEOBJECTTYPE",
                related_name="informatieobjecttypen",
                through="datamodel.ZaakInformatieobjectType",
                to="datamodel.ZaakType",
                verbose_name="zaaktypes",
            ),
        ),
    ]
