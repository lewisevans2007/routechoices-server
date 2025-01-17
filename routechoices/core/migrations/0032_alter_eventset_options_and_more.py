# Generated by Django 4.1.2 on 2022-11-11 13:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0031_eventset_event_event_set"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eventset",
            options={"ordering": ["-creation_date", "name"]},
        ),
        migrations.AlterUniqueTogether(
            name="eventset",
            unique_together={("club", "name")},
        ),
    ]
