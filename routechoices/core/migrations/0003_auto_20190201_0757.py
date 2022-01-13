# Generated by Django 2.1.5 on 2019-02-01 07:57

import django.db.models.deletion
from django.db import migrations, models

import routechoices.core.models
import routechoices.lib
import routechoices.lib.helpers
import routechoices.lib.storages


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_event_end_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Map",
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
                (
                    "aid",
                    models.CharField(
                        default=routechoices.lib.helpers.random_key,
                        editable=False,
                        max_length=12,
                        unique=True,
                    ),
                ),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("modification_date", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "image",
                    models.ImageField(
                        height_field="height",
                        storage=routechoices.lib.storages.OverwriteImageStorage(
                            aws_s3_bucket_name="routechoices-maps"
                        ),
                        upload_to=routechoices.core.models.map_upload_path,
                        width_field="width",
                    ),
                ),
                (
                    "height",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "width",
                    models.PositiveIntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "corners_coordinates",
                    models.CharField(
                        help_text="Latitude and longitude of map corners separated by commasin following order Top Left, Top right, Bottom Right, Bottom left. eg: 60.519,22.078,60.518,22.115,60.491,22.112,60.492,22.073",
                        max_length=255,
                        validators=[
                            routechoices.lib.validators.validate_corners_coordinates
                        ],
                    ),
                ),
                (
                    "club",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="maps",
                        to="core.Club",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "maps",
                "ordering": ["-creation_date"],
                "verbose_name": "map",
            },
        ),
        migrations.RemoveField(
            model_name="event",
            name="image_height",
        ),
        migrations.RemoveField(
            model_name="event",
            name="image_width",
        ),
        migrations.RemoveField(
            model_name="event",
            name="map_corners_coordinates",
        ),
        migrations.AlterField(
            model_name="event",
            name="map",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="core.Map",
            ),
        ),
    ]
