# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0011_auto_20140811_0649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snstoken',
            name='sns_reg_id',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
