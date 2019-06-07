# Generated by Django 2.2.2 on 2019-06-07 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0014_auto_20190523_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='allow_route_upload',
            field=models.BooleanField(default=False, help_text='Participants can upload their routes after the event.'),
        ),
        migrations.AlterField(
            model_name='event',
            name='open_registration',
            field=models.BooleanField(default=False, help_text='Participants can register themselves to the event.'),
        ),
        migrations.CreateModel(
            name='DeviceOwnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to='core.Device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='owners',
            field=models.ManyToManyField(related_name='devices', through='core.DeviceOwnership', to=settings.AUTH_USER_MODEL),
        ),
    ]
