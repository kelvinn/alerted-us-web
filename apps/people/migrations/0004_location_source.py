# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_location_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='source',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'static', b'Static'), (b'dynamic', b'Dynamic (e.g. mobile device)')]),
            preserve_default=True,
        ),
    ]
