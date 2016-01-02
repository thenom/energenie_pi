# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0014_auto_20160102_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='off_complete',
        ),
        migrations.AddField(
            model_name='timeslot',
            name='off_complete',
            field=models.ManyToManyField(related_name='off_complete', to='powersocket.Schedule'),
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='on_complete',
        ),
        migrations.AddField(
            model_name='timeslot',
            name='on_complete',
            field=models.ManyToManyField(related_name='on_complete', to='powersocket.Schedule'),
        ),
    ]
