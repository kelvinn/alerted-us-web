# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0003_parameter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cap_resource_desc', models.CharField(max_length=500)),
                ('cap_mime_type', models.CharField(max_length=75)),
                ('cap_size', models.CharField(max_length=75)),
                ('cap_uri', models.URLField(blank=True)),
                ('cap_deref_rui', models.URLField(blank=True)),
                ('cap_digest', models.CharField(max_length=75)),
                ('cap_info', models.ForeignKey(to_field='id', blank=True, to='alertdb.Info', null=True,
                                               on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
