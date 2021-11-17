# Generated by Django 2.2.4 on 2021-11-16 16:20

from django.db import migrations, models
import django.db.models.deletion
import uuid
import ztc.datamodel.validators


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0126_merge_20201027_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZaakObjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_etag', models.CharField(editable=False, help_text='MD5 hash of the resource representation in its current version.', max_length=32, verbose_name='etag value')),
                ('uuid', models.UUIDField(default=uuid.uuid4, help_text='Unieke resource identifier (UUID4)', unique=True)),
                ('ander_objecttype', models.BooleanField(help_text='Aanduiding waarmee wordt aangegeven of het ZAAKOBJECTTYPE een ander, niet in RSGB en RGBZ voorkomend, objecttype betreft.', verbose_name='Ander objecttype')),
                ('begin_geldigheid', models.DateField(help_text='De datum waarop het ZAAKOBJECTTYPE is ontstaan.', verbose_name='Begin geldigheid')),
                ('einde_geldigheid', models.DateField(blank=True, help_text='De datum waarop het ZAAKOBJECTTYPE is opgeheven.', null=True, verbose_name='Einde geldigheid')),
                ('objecttype', models.CharField(blank=True, help_text='De naam van het objecttype waarop zaken van het gerelateerde ZAAKTYPE betrekking hebben.', max_length=40, null=True, validators=[ztc.datamodel.validators.validate_letters_numbers_underscores_spaces], verbose_name='Objecttype')),
                ('relatie_omschrijving', models.CharField(help_text='Omschrijving van de betrekking van het Objecttype op zaken van het gerelateerde ZAAKTYPE.', max_length=255, verbose_name='Relatie omschrijving')),
                ('catalogus', models.ForeignKey(help_text='URL-referentie naar de CATALOGUS waartoe dit ZAAKOBJECTTYPE behoort.', on_delete=django.db.models.deletion.CASCADE, to='datamodel.Catalogus', verbose_name='Catalogus')),
                ('zaaktype', models.ForeignKey(help_text='URL-referentie naar de ZAAKTYPE waartoe dit ZAAKOBJECTTYPE behoort.', on_delete=django.db.models.deletion.CASCADE, related_name='objecttypen', to='datamodel.ZaakType', verbose_name='Zaaktype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
