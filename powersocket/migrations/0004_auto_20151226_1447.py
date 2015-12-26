# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0003_schedule_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='days_of_week',
            field=models.IntegerField(default=0),
        ),
    ]
