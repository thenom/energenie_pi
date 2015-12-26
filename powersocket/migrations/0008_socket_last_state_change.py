# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0007_auto_20151226_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='socket',
            name='last_state_change',
            field=models.CharField(default=b'm', max_length=1, choices=[(b'm', b'Manual'), (b's', b'Schedule')]),
        ),
    ]
