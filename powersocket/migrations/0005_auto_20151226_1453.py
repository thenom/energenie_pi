# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powersocket', '0004_auto_20151226_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaysOfTheWeek',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='schedule',
            name='days_of_week',
            field=models.ForeignKey(to='powersocket.DaysOfTheWeek'),
        ),
    ]
