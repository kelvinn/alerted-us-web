# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0007_auto_20140721_0104'),
    ]

    operations = [
        migrations.CreateModel(
            name='SNSToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('sns_reg_id', models.CharField(max_length=200, null=True, blank=True)),
                ('sns_endpoint_apn', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='location',
            name='date_received',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
