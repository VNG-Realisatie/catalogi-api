# Generated by Django 2.0.9 on 2019-02-21 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("datamodel", "0084_auto_20190220_1817")]

    operations = [
        migrations.AddField(
            model_name="resultaattype",
            name="brondatum_archiefprocedure_datumkenmerk",
            field=models.CharField(
                blank=True,
                help_text="Naam van de attribuutsoort van het procesobject dat bepalend is voor het einde van de procestermijn.",
                max_length=80,
                verbose_name="datumkenmerk",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="brondatum_archiefprocedure_einddatum_bekend",
            field=models.BooleanField(
                default=False,
                help_text="Indicatie dat de einddatum van het procesobject gedurende de uitvoering van de zaak bekend moet worden. Indien deze nog niet bekend is en deze waarde staat op `true`, dan kan de zaak (nog) niet afgesloten worden.",
                verbose_name="einddatum bekend",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="brondatum_archiefprocedure_objecttype",
            field=models.CharField(
                blank=True,
                choices=[("besluit", "Besluit"), ("zaak", "Zaak")],
                help_text="Het soort object in de registratie dat het procesobject representeert.",
                max_length=80,
                verbose_name="objecttype",
            ),
        ),
        migrations.AddField(
            model_name="resultaattype",
            name="brondatum_archiefprocedure_registratie",
            field=models.CharField(
                blank=True,
                help_text="De naam van de registratie waarvan het procesobject deel uit maakt.",
                max_length=80,
                verbose_name="registratie",
            ),
        ),
    ]
