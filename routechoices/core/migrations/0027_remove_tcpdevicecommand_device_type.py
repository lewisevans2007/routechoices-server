# Generated by Django 4.1 on 2022-08-09 05:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0026_alter_tcpdevicecommand_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tcpdevicecommand",
            name="device_type",
        ),
    ]
