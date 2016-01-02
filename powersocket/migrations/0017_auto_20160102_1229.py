# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0016_auto_20160102_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='last_day_check',
        ),
        migrations.AddField(
            model_name='schedule',
            name='last_day_check',
            field=models.ForeignKey(default=0, to='powersocket.DaysOfTheWeek'),
            preserve_default=False,
        ),
    ]
