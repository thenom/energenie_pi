# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0019_auto_20160102_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socket',
            name='last_state_change',
        ),
        migrations.RemoveField(
            model_name='socket',
            name='schedule_override',
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.TimeField(help_text=b'Seconds are ignored'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.TimeField(help_text=b'Seconds are ignored'),
        ),
    ]
