# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0008_socket_last_state_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='overridden',
            field=models.BooleanField(default=0),
        ),
    ]
