# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0005_auto_20180813_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='ips',
            name='description',
            field=models.CharField(default=b'', max_length=200, null=True),
        ),
    ]
