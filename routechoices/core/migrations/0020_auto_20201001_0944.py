# Generated by Django 3.1.2 on 2020-10-01 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_auto_20201001_0715"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imeidevice",
            name="device",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="physical_device",
                to="core.device",
            ),
        ),
    ]
