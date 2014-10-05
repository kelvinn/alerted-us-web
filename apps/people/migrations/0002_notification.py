# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertdb', '0002_area'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(to_field='id', blank=True, to='people.Location', null=True)),
                ('cap_area', models.ForeignKey(to_field='id', blank=True, to='alertdb.Area', null=True)),
                ('message_id', models.CharField(max_length=300, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
