# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0010_snstoken_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='snstoken',
            name='sns_device_id',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='snstoken',
            name='unique_id',
        ),
    ]
