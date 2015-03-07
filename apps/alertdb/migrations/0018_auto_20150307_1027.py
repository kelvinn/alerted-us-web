# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0017_auto_20141219_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='cap_date_received',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_sender',
            field=models.CharField(db_index=True, max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alert',
            name='cap_sent',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='info',
            name='cap_expires',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
