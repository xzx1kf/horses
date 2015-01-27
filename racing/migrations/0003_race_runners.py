# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('racing', '0002_auto_20150126_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='runners',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
