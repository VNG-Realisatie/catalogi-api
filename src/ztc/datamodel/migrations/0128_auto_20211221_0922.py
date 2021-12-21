# Generated by Django 2.2.4 on 2021-12-21 09:22

import django.db.models.deletion
from django.db import migrations, models

import relativedeltafield


class Migration(migrations.Migration):

    dependencies = [
        ("datamodel", "0127_auto_20211119_1358"),
    ]

    operations = [
        migrations.AddField(
            model_name="catalogus",
            name="datum_begin_versie",
            field=models.DateField(
                blank=True,
                help_text="Datum waarop de versie van de zaaktypecatalogus van toepassing is geworden.",
                null=True,
                verbose_name="begindatum versie",
            ),
        ),
        migrations.AddField(
            model_name="catalogus",
            name="naam",
            field=models.CharField(
                blank=True,
                help_text="De benaming die is gegeven aan de zaaktypecatalogus.",
                max_length=200,
                null=True,
                verbose_name="naam",
            ),
        ),
        migrations.AddField(
            model_name="catalogus",
            name="versie",
            field=models.CharField(
                blank=True,
                help_text="Versie-aanduiding van de van toepassing zijnde zaaktypecatalogus.",
                max_length=20,
                null=True,
                verbose_name="versie",
            ),
        ),
        migrations.AddField(
            model_name="eigenschap",
            name="datum_begin_geldigheid",
            field=models.DateField(
                blank=True,
                help_text="De datum waarop het is ontstaan.",
                null=True,
                verbose_name="datum begin geldigheid",
            ),
        ),
        migrations.AddField(
            model_name="eigenschap",
            name="datum_einde_geldigheid",
            field=models.DateField(
                blank=True,
                help_text="De datum waarop het is opgeheven.",
                null=True,
                verbose_name="datum einde geldigheid",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="catalogus",
            field=models.ForeignKey(
                blank=True,
                help_text="URL-referentie naar de CATALOGUS waartoe dit RESULTAATTYPE behoort.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="datamodel.Catalogus",
                verbose_name="catalogus",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="datum_begin_geldigheid",
            field=models.DateField(
                blank=True,
                help_text="De datum waarop het is ontstaan.",
                null=True,
                verbose_name="datum begin geldigheid",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="datum_einde_geldigheid",
            field=models.DateField(
                blank=True,
                help_text="De datum waarop het is opgeheven.",
                null=True,
                verbose_name="datum einde geldigheid",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="indicatie_specifiek",
            field=models.BooleanField(
                blank=True,
                help_text="Aanduiding of het, vanuit archiveringsoptiek, een resultaattype betreft dat specifiek is voor een bepaalde procesobjectaard.",
                null=True,
                verbose_name="indicatie specifiek",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="informatieobjecttypen",
            field=models.ManyToManyField(
                blank=True,
                help_text="De INFORMATIEOBJECTTYPEn die verplicht aanwezig moeten zijn in het zaakdossier van ZAAKen van dit ZAAKTYPE voordat een resultaat van dit RESULTAATTYPE kan worden gezet.",
                to="datamodel.InformatieObjectType",
                verbose_name="informatieobjecttypen",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="procesobjectaard",
            field=models.CharField(
                blank=True,
                help_text="Omschrijving van het object, subject of gebeurtenis waarop, vanuit archiveringsoptiek, het resultaattype bij zaken van dit type betrekking heeft.",
                max_length=200,
                null=True,
                verbose_name="procesobjectaard",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="procestermijn",
            field=relativedeltafield.RelativeDeltaField(
                blank=True,
                help_text="De periode dat het zaakdossier na afronding van de zaak actief gebruikt en/of geraadpleegd wordt ter ondersteuning van de taakuitoefening van de organisatie.",
                null=True,
                verbose_name="procestermijn",
            ),
        ),
        migrations.AddField(
            model_name="roltype",
            name="catalogus",
            field=models.ForeignKey(
                blank=True,
                help_text="URL-referentie naar de CATALOGUS waartoe dit ROLTYPE behoort.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="datamodel.Catalogus",
                verbose_name="catalogus",
            ),
        ),
        migrations.AddField(
            model_name="roltype",
            name="datum_begin_geldigheid",
            field=models.DateField(
                blank=True,
                help_text="De datum waarop het is ontstaan.",
                null=True,
                verbose_name="datum begin geldigheid",
            ),
        ),
        migrations.AddField(
            model_name="roltype",
            name="datum_einde_geldigheid",
            field=models.DateField(
                blank=True,
                help_text="De datum waarop het is opgeheven.",
                null=True,
                verbose_name="datum einde geldigheid",
            ),
        ),
        migrations.AddField(
            model_name="statustype",
            name="datum_begin_geldigheid",
            field=models.DateField(
                blank=True,
                help_text="De datum waarop het is ontstaan.",
                null=True,
                verbose_name="datum begin geldigheid",
            ),
        ),
        migrations.AddField(
            model_name="statustype",
            name="datum_einde_geldigheid",
            field=models.DateField(
                blank=True,
                help_text="De datum waarop het is opgeheven.",
                null=True,
                verbose_name="datum einde geldigheid",
            ),
        ),
        migrations.AddField(
            model_name="statustype",
            name="eigenschappen",
            field=models.ManyToManyField(
                blank=True,
                help_text="de EIGENSCHAPpen die verplicht een waarde moeten hebben gekregen, voordat een STATUS van dit STATUSTYPE kan worden gezet.",
                related_name="statustypen",
                to="datamodel.Eigenschap",
                verbose_name="eigenschappen",
            ),
        ),
        migrations.AlterField(
            model_name="catalogus",
            name="contactpersoon_beheer_naam",
            field=models.CharField(
                help_text="De naam van de contactpersoon die verantwoordelijk is voor het beheer van de CATALOGUS.",
                max_length=40,
                verbose_name="naam contactpersoon",
            ),
        ),
        migrations.AlterField(
            model_name="informatieobjecttype",
            name="zaaktypen",
            field=models.ManyToManyField(
                blank=True,
                help_text="ZAAKTYPE met ZAAKen die relevant kunnen zijn voor dit INFORMATIEOBJECTTYPE",
                related_name="informatieobjecttypen",
                through="datamodel.ZaakInformatieobjectType",
                to="datamodel.ZaakType",
                verbose_name="zaaktypen",
            ),
        ),
        migrations.AlterField(
            model_name="resultaattype",
            name="brondatum_archiefprocedure_procestermijn",
            field=relativedeltafield.RelativeDeltaField(
                blank=True,
                help_text="De periode dat het zaakdossier na afronding van de zaak actief gebruikt en/of geraadpleegd wordt ter ondersteuning van de taakuitoefening van de organisatie. Enkel relevant indien de afleidingswijze 'termijn' is.",
                null=True,
                verbose_name="brondatum procestermijn",
            ),
        ),
    ]
