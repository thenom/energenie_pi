# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0013_auto_20151227_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='off_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='on_complete',
            field=models.BooleanField(default=False),
        ),
    ]
