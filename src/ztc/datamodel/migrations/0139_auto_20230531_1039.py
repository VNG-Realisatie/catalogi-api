# Generated by Django 3.2.14 on 2023-05-31 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datamodel", "0138_alter_zaaktypenrelatie_unique_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="informatieobjecttype",
            name="zaaktypen",
        ),
        migrations.AlterField(
            model_name="zaakinformatieobjecttype",
            name="informatieobjecttype",
            field=models.CharField(max_length=100),
        ),
    ]
