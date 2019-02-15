# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0010_ippools_excute_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='ippools',
            name='threshold',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
