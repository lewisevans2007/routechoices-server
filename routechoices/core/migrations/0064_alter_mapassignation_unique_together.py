# Generated by Django 5.0.1 on 2024-03-06 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0063_alter_event_list_on_routechoices_com"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="mapassignation",
            unique_together=set(),
        ),
    ]
