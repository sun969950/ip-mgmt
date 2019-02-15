# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0011_ippools_threshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='ippools',
            name='use_rate',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
