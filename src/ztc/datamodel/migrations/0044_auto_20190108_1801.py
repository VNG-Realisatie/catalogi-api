# Generated by Django 2.0.9 on 2019-01-08 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("datamodel", "0043_auto_20190108_1750")]

    operations = [
        migrations.AlterField(
            model_name="zaaktype",
            name="handeling_behandelaar",
            field=models.CharField(
                help_text="Werkwoord dat hoort bij de handeling die de behandelaar verricht bij het afdoen van ZAAKen van dit ZAAKTYPE. Meestal 'behandelen', 'uitvoeren', 'vaststellen' of 'onderhouden'. Zie ook het IOB model op https://www.gemmaonline.nl/index.php/Imztc_2.1/doc/attribuutsoort/zaaktype.handeling_behandelaar",
                max_length=20,
                verbose_name="handeling behandelaar",
            ),
        )
    ]
