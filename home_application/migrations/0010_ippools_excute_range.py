# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0009_ippools_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='ippools',
            name='excute_range',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
