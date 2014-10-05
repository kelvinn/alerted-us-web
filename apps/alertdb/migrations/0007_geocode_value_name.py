# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0006_geocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='geocode',
            name='value_name',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'fips6', b'FIPS6'), (b'taiwan', b'Taiwan Townships')]),
            preserve_default=True,
        ),
    ]
