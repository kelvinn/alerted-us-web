# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0008_auto_20140607_1502'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Fips6',
        ),
        migrations.DeleteModel(
            name='TaiwanGeocode',
        ),
    ]
