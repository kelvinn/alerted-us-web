# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0012_auto_20140811_1139'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SNSToken',
        ),
    ]
