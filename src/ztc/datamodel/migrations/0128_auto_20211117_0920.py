# Generated by Django 2.2.4 on 2021-11-17 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0127_zaakobjecttype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zaakobjecttype',
            options={'ordering': ('catalogus', 'begin_geldigheid'), 'verbose_name': 'Zaakobjecttype', 'verbose_name_plural': 'Zaakobjecttypen'},
        ),
    ]
