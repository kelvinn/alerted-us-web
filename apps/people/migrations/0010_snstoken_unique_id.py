# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0009_auto_20140728_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='snstoken',
            name='unique_id',
            field=models.CharField(max_length=200, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
