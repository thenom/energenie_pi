# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0015_auto_20160102_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='off_complete',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='on_complete',
        ),
        migrations.AddField(
            model_name='schedule',
            name='last_day_check',
            field=models.ManyToManyField(to='powersocket.DaysOfTheWeek'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='time_slots_off_complete',
            field=models.ManyToManyField(related_name='time_slot_off', to='powersocket.TimeSlot'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='time_slots_on_complete',
            field=models.ManyToManyField(related_name='time_slot_on', to='powersocket.TimeSlot'),
        ),
    ]
