# Generated by Django 4.1 on 2022-08-11 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invitations", "0006_alter_invitation_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invitation",
            name="sent",
            field=models.DateTimeField(blank=True, null=True, verbose_name="sent"),
        ),
    ]
