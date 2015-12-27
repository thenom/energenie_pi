# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0012_auto_20151227_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daysoftheweek',
            name='day',
            field=models.CharField(unique=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='socket',
            name='socket_id',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
