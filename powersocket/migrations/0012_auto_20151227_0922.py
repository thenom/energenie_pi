# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0011_auto_20151226_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='overridden',
        ),
        migrations.AddField(
            model_name='socket',
            name='schedule_override',
            field=models.BooleanField(default=False),
        ),
    ]
