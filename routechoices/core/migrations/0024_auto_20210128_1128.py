# Generated by Django 3.1.4 on 2021-01-28 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_auto_20201217_0743"),
    ]

    operations = [
        migrations.CreateModel(
            name="MapAssignation",
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
                ("title", models.CharField(max_length=255)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="map_assignations",
                        to="core.event",
                    ),
                ),
                (
                    "map",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="map_assignations",
                        to="core.map",
                    ),
                ),
            ],
            options={
                "unique_together": {("map", "event")},
            },
        ),
        migrations.AddField(
            model_name="event",
            name="extra_maps",
            field=models.ManyToManyField(
                related_name="_event_extra_maps_+",
                through="core.MapAssignation",
                to="core.Map",
            ),
        ),
    ]
