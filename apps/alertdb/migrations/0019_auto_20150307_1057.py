# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0018_auto_20150307_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(db_index=True, srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
    ]
