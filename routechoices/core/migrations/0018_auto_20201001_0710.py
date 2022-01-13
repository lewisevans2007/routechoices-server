# Generated by Django 3.1.2 on 2020-10-01 07:10

import re

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import routechoices.lib.helpers
import routechoices.lib.validators


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_device_locations_raw"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="aid",
            field=models.CharField(
                default=routechoices.lib.helpers.short_random_key,
                max_length=12,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^[-a-zA-Z0-9_]+\\Z"),
                        "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                        "invalid",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="device",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.device"
            ),
        ),
        migrations.CreateModel(
            name="ImeiDevice",
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
                    "imei",
                    models.CharField(
                        max_length=32,
                        unique=True,
                        validators=[routechoices.lib.validators.validate_imei],
                    ),
                ),
                (
                    "device",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="physical_device",
                        to="core.device",
                    ),
                ),
            ],
            options={
                "verbose_name": "imei device",
                "verbose_name_plural": "imei devices",
                "ordering": ["imei"],
            },
        ),
    ]
