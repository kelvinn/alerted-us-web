# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0012_auto_20140611_0512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='cap_digest',
            field=models.CharField(max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='cap_resource_desc',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='cap_size',
            field=models.CharField(max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='cap_mime_type',
            field=models.CharField(max_length=75, null=True, blank=True),
        ),
    ]
