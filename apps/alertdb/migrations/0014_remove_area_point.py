# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0013_auto_20140611_0521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='point',
        ),
    ]
