# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0016_auto_20141114_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='cap_id',
            field=models.CharField(max_length=500, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geocode',
            name='value_name',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'FIPS6', b'FIPS6'), (b'Taiwan_Geocode_100', b'Taiwan Townships'), (b'SAME', b'SAME')]),
            preserve_default=True,
        ),
    ]
