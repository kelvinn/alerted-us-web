# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0008_auto_20140728_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='snstoken',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='snstoken',
            name='sns_reg_id',
            field=models.CharField(max_length=200, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='snstoken',
            name='sns_endpoint_apn',
            field=models.CharField(max_length=200, unique=True, null=True, blank=True),
        ),
    ]
