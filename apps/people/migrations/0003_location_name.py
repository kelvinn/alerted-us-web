# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='name',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
