# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0006_ips_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ips',
            name='is_assigned',
        ),
    ]
