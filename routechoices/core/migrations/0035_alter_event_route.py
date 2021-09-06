# Generated by Django 3.2.4 on 2021-07-13 06:03

from django.db import migrations, models
import routechoices.core.models
import routechoices.lib.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_event_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='route',
            field=models.FileField(blank=True, help_text='Optional GPX file to be overlayed on the map', null=True, upload_to=routechoices.core.models.route_upload_path),
        ),
    ]
