# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0004_location_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('date_received', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='location',
            name='source',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'static', b'Static'), (b'current', b'Current Location')]),
        ),
    ]
