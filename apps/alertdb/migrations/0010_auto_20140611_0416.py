# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0009_auto_20140607_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='cap_sender',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_addresses',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_source',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_id',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_incidents',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_note',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_message_type',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'Alert', b'Alert'), (b'Update', b'Update'), (b'Cancel', b'Cancel'), (b'Ack', b'Ack'), (b'Error', b'Error')]),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_references',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_restriction',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_scope',
            field=models.CharField(blank=True, max_length=15, null=True, choices=[(b'Public', b'Public'), (b'Restricted', b'Restricted'), (b'Private', b'Private')]),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_status',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'Actual', b'Actual'), (b'System', b'System'), (b'Exercise', b'Exercise'), (b'Test', b'Test'), (b'Draft', b'Draft')]),
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_code',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
