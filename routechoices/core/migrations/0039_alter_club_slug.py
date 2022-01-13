# Generated by Django 3.2.5 on 2021-07-29 19:30

from django.db import migrations, models

import routechoices.lib.validators


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0038_auto_20210713_0756"),
    ]

    operations = [
        migrations.AlterField(
            model_name="club",
            name="slug",
            field=models.CharField(
                help_text="This is used in the urls of your events",
                max_length=50,
                unique=True,
                validators=[routechoices.lib.validators.validate_domain_slug],
            ),
        ),
    ]
