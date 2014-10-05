# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0004_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='cap_slug',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_category',
            field=models.CharField(max_length=15, choices=[(b'Geo', b'Geo'), (b'Met', b'Meteorological'), (b'Safety', b'Safety'), (b'Security', b'Security'), (b'Rescue', b'Rescue'), (b'Fire', b'Fire'), (b'Health', b'Health'), (b'Env', b'Env'), (b'Transport', b'Transport'), (b'Infra', b'Infrastructure'), (b'CBRNE', b'CBRNE'), (b'Other', b'Other')]),
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_urgency',
            field=models.CharField(max_length=15, choices=[(b'Immediate', b'Immediate'), (b'Expected', b'Expected'), (b'Future', b'Future'), (b'Past', b'Past'), (b'Unknown', b'Unknown')]),
        ),
    ]
