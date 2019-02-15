# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0007_remove_ips_is_assigned'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CMDBUsedIPs',
        ),
    ]
