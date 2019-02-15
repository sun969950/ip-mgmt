# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0013_ips_work_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='ippools',
            name='gateway',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ippools',
            name='mask',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ips',
            name='gateway',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ips',
            name='mask',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
