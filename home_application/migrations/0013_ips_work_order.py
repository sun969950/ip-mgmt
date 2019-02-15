# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0012_ippools_use_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='ips',
            name='work_order',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
