# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0006_daysoftheweek_python_dayofweek'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='days_of_week',
        ),
        migrations.AddField(
            model_name='schedule',
            name='days_of_week',
            field=models.ManyToManyField(to='powersocket.DaysOfTheWeek'),
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='socket',
        ),
        migrations.AddField(
            model_name='schedule',
            name='socket',
            field=models.ManyToManyField(to='powersocket.Socket'),
        ),
    ]
