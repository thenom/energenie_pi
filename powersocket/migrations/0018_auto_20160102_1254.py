# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0017_auto_20160102_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='time_slots',
            field=models.ManyToManyField(to='powersocket.TimeSlot', blank=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='time_slots_off_complete',
            field=models.ManyToManyField(related_name='time_slot_off', to='powersocket.TimeSlot', blank=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='time_slots_on_complete',
            field=models.ManyToManyField(related_name='time_slot_on', to='powersocket.TimeSlot', blank=True),
        ),
    ]
