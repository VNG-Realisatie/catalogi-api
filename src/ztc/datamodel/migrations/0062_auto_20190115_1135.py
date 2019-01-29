# Generated by Django 2.0.9 on 2019-01-15 10:35

from django.db import migrations
import zds_schema.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0061_delete_referentieproces'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogus',
            name='rsin',
            field=zds_schema.fields.RSINField(help_text='Het door een kamer toegekend uniek nummer voor de INGESCHREVEN NIET-NATUURLIJK PERSOON die de eigenaar is van een CATALOGUS.', max_length=9, verbose_name='rsin'),
        ),
    ]
