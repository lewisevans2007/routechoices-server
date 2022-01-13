# Generated by Django 3.2.9 on 2021-11-20 09:45

from django.db import migrations, models

import routechoices.core.models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0053_rename_username_chatmessage_nickname"),
    ]

    operations = [
        migrations.AddField(
            model_name="club",
            name="logo",
            field=models.ImageField(
                blank=True,
                help_text="Square image of width greater or equal to 128px",
                null=True,
                upload_to=routechoices.core.models.logo_upload_path,
            ),
        ),
    ]
