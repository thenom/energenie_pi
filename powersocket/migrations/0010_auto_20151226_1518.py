# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0009_schedule_overridden'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlots',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('days_of_week', models.ManyToManyField(to='powersocket.DaysOfTheWeek')),
            ],
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='days_of_week',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='start_time',
        ),
        migrations.AddField(
            model_name='schedule',
            name='time_slots',
            field=models.ManyToManyField(to='powersocket.TimeSlots'),
        ),
    ]
