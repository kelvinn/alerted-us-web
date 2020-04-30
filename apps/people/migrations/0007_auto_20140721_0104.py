# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20140720_0526'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='cap_info',
            field=models.ForeignKey(to_field='id', blank=True, to='alertdb.Info', null=True,
                                    on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='notification',
            name='cap_area',
        ),
    ]
