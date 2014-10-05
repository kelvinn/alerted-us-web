# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0002_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value_name', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=500)),
                ('cap_info', models.ForeignKey(to_field='id', blank=True, to='alertdb.Info', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
