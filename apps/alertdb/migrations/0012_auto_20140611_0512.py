# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0011_auto_20140611_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='cap_instruction',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_contact',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
