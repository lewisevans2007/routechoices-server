# Generated by Django 4.1 on 2022-08-09 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0024_rename_queclink300command_queclinkcommand"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="QueclinkCommand",
            new_name="TcpDeviceCommand",
        ),
        migrations.AddField(
            model_name="tcpdevicecommand",
            name="device_type",
            field=models.CharField(max_length=16),
        ),
    ]