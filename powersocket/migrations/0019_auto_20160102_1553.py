# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0018_auto_20160102_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='last_day_check',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='time_slots_off_complete',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='time_slots_on_complete',
        ),
    ]
