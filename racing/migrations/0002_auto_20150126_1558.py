# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('racing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='horse',
            name='forecast',
            field=models.DecimalField(default=0, decimal_places=1, max_digits=4),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='horse',
            name='last_run',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='horse',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='horse',
            name='weight',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meeting',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 1, 26, 15, 58, 40, 630851, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='race',
            name='distance',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='race',
            name='going',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
