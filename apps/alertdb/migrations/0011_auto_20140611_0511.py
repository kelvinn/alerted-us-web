# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0010_auto_20140611_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='cap_event',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_urgency',
            field=models.CharField(blank=True, max_length=15, null=True, choices=[(b'Immediate', b'Immediate'), (b'Expected', b'Expected'), (b'Future', b'Future'), (b'Past', b'Past'), (b'Unknown', b'Unknown')]),
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_sender_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_audience',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_event_code',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_response_type',
            field=models.CharField(blank=True, max_length=15, null=True, choices=[(b'Shelter', b'Shelter'), (b'Evacuate', b'Evacuate'), (b'Prepare', b'Prepare'), (b'Execute', b'Execute'), (b'Avoid', b'Avoid'), (b'Monitor', b'Monitor'), (b'Assess', b'Assess'), (b'AllClear', b'AllClear'), (b'None', b'None')]),
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_language',
            field=models.CharField(max_length=75, null=True, blank=True),
        ),
    ]
