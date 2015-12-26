# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0002_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='description',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
