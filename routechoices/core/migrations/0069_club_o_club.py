# Generated by Django 5.0.4 on 2024-05-19 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0068_remove_event_emergency_contact_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="club",
            name="o_club",
            field=models.BooleanField(
                default=False, verbose_name="Is an orienteering club"
            ),
        ),
    ]