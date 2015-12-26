# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Socket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('socket_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=200)),
                ('current_state', models.BooleanField(default=0)),
            ],
        ),
    ]
