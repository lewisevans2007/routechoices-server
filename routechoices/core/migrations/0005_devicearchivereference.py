# Generated by Django 4.0.3 on 2022-04-06 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_event_send_interval"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeviceArchiveReference",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                (
                    "archive",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="original_ref",
                        to="core.device",
                    ),
                ),
                (
                    "original",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="archives_ref",
                        to="core.device",
                    ),
                ),
            ],
        ),
    ]