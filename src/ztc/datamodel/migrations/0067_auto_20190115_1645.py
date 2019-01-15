# Generated by Django 2.0.9 on 2019-01-15 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0066_zaaktype_selectielijst_procestype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zaaktypenrelatie',
            name='toelichting',
            field=models.CharField(blank=True, default='', help_text='Een toelichting op de aard van de relatie tussen beide ZAAKTYPEN.', max_length=255, verbose_name='toelichting'),
            preserve_default=False,
        ),
    ]