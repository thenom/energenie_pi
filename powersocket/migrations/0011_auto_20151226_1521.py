# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0010_auto_20151226_1518'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TimeSlots',
            new_name='TimeSlot',
        ),
    ]
