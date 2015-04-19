# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0013_delete_snstoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='cap_info',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
