# Generated by Django 3.2.4 on 2021-07-13 05:56

from django.db import migrations, models
import routechoices.core.models
import routechoices.lib.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20210713_0535'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='route',
            field=models.FileField(help_text='Optional GPX file to be overlayed on the map', null=True, upload_to=routechoices.core.models.route_upload_path),
        ),
    ]
