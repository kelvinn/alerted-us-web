# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0007_geocode_value_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='cap_raw',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geocode',
            name='value_name',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'FIPS6', b'FIPS6'), (b'Taiwan_Geocode_100', b'Taiwan Townships')]),
        ),
    ]
