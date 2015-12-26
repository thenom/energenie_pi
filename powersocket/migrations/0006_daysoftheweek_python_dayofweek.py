# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0005_auto_20151226_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='daysoftheweek',
            name='python_dayofweek',
            field=models.IntegerField(default=0),
        ),
    ]
