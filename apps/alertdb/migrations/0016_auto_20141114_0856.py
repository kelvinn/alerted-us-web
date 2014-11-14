# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0015_alert_contributor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='cap_id',
            field=models.CharField(max_length=500, unique=True, null=True),
            preserve_default=True,
        ),
    ]
