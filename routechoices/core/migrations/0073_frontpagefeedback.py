# Generated by Django 5.1 on 2024-08-30 11:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0072_alter_club_domain"),
    ]

    operations = [
        migrations.CreateModel(
            name="FrontPageFeedback",
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
                ("content", models.TextField(max_length=140)),
                (
                    "stars",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MaxValueValidator(5)]
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("club_name", models.CharField(max_length=50)),
            ],
        ),
    ]