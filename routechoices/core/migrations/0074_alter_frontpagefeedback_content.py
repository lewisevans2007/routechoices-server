# Generated by Django 5.1 on 2024-08-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0073_frontpagefeedback"),
    ]

    operations = [
        migrations.AlterField(
            model_name="frontpagefeedback",
            name="content",
            field=models.TextField(max_length=255),
        ),
    ]