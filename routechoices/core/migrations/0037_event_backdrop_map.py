# Generated by Django 3.2.4 on 2021-07-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20210713_0535'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='backdrop_map',
            field=models.CharField(choices=[('osm', 'Open Street Map'), ('gmap-street', 'Google Map Street'), ('gmap-hybrid', 'Google Map Satellite'), ('mapant-fi', 'Mapant Finland'), ('mapant-no', 'Mapant Norway'), ('mapant-es', 'Mapant Spain'), ('topo-fi', 'Topo Finland'), ('topo-no', 'Topo Norway')], default='osm', max_length=16),
        ),
    ]
