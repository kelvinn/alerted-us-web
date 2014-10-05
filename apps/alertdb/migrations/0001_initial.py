# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaiwanGeocode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('nativename', models.CharField(max_length=200, null=True, blank=True)),
                ('geocode_num', models.CharField(max_length=200, null=True, blank=True)),
                ('town_name', models.CharField(max_length=200, null=True, blank=True)),
                ('shape_leng', models.FloatField(null=True, blank=True)),
                ('fe_area', models.FloatField(null=True, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fips6',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=2)),
                ('cwa', models.CharField(max_length=9)),
                ('countyname', models.CharField(max_length=24)),
                ('fips', models.CharField(max_length=5)),
                ('time_zone', models.CharField(max_length=2)),
                ('fe_area', models.CharField(max_length=2)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cap_id', models.CharField(max_length=500)),
                ('cap_sender', models.CharField(max_length=200)),
                ('cap_sent', models.DateTimeField(null=True, blank=True)),
                ('cap_status', models.CharField(max_length=10, choices=[(b'Actual', b'Actual'), (b'System', b'System'), (b'Exercise', b'Exercise'), (b'Test', b'Test'), (b'Draft', b'Draft')])),
                ('cap_message_type', models.CharField(max_length=10, choices=[(b'Alert', b'Alert'), (b'Update', b'Update'), (b'Cancel', b'Cancel'), (b'Ack', b'Ack'), (b'Error', b'Error')])),
                ('cap_source', models.CharField(max_length=500)),
                ('cap_scope', models.CharField(max_length=15, choices=[(b'Public', b'Public'), (b'Restricted', b'Restricted'), (b'Private', b'Private')])),
                ('cap_restriction', models.TextField()),
                ('cap_addresses', models.CharField(max_length=500)),
                ('cap_code', models.CharField(max_length=500)),
                ('cap_note', models.TextField()),
                ('cap_references', models.TextField()),
                ('cap_incidents', models.CharField(max_length=500)),
                ('cap_date_received', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cap_language', models.CharField(max_length=75)),
                ('cap_category', models.CharField(max_length=15, choices=[(b'Geo', b'Geo'), (b'Met', b'Met'), (b'Safety', b'Safety'), (b'Security', b'Security'), (b'Rescue', b'Rescue'), (b'Fire', b'Fire'), (b'Health', b'Health'), (b'Env', b'Env'), (b'Transport', b'Transport'), (b'Infra', b'Infra'), (b'CBRNE', b'CBRNE'), (b'Other', b'Other'), (b'abc', b'abc'), (b'abc', b'abc')])),
                ('cap_event', models.CharField(max_length=500)),
                ('cap_response_type', models.CharField(max_length=15, choices=[(b'Shelter', b'Shelter'), (b'Evacuate', b'Evacuate'), (b'Prepare', b'Prepare'), (b'Execute', b'Execute'), (b'Avoid', b'Avoid'), (b'Monitor', b'Monitor'), (b'Assess', b'Assess'), (b'AllClear', b'AllClear'), (b'None', b'None')])),
                ('cap_urgency', models.CharField(max_length=15, choices=[(b'Immediate', b'Immediate'), (b'Expected', b'Expected'), (b'Future', b'Future'), (b'Past', b'Past'), (b'Unknown', b'Unknown'), (b'abc', b'abc')])),
                ('cap_severity', models.CharField(max_length=15, choices=[(b'Extreme', b'Extreme'), (b'Severe', b'Severe'), (b'Moderate', b'Moderate'), (b'Minor', b'Minor'), (b'Unknown', b'Unknown')])),
                ('cap_certainty', models.CharField(max_length=15, choices=[(b'Observed', b'Observed'), (b'Likely', b'Likely'), (b'Possible', b'Possible'), (b'Unlikely', b'Unlikely'), (b'Unknown', b'Unknown')])),
                ('cap_audience', models.CharField(max_length=500)),
                ('cap_event_code', models.CharField(max_length=500)),
                ('cap_effective', models.DateTimeField(null=True, blank=True)),
                ('cap_onset', models.DateTimeField(null=True, blank=True)),
                ('cap_expires', models.DateTimeField(null=True, blank=True)),
                ('cap_sender_name', models.CharField(max_length=200)),
                ('cap_headline', models.CharField(max_length=500)),
                ('cap_description', models.TextField()),
                ('cap_instruction', models.TextField()),
                ('cap_link', models.URLField(blank=True)),
                ('cap_contact', models.CharField(max_length=500)),
                ('cap_alert', models.ForeignKey(to_field='id', blank=True, to='alertdb.Alert', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
