# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_initial_settings_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcludeIPs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=15)),
                ('ip_pool', models.ForeignKey(to='home_application.IPPools')),
            ],
        ),
    ]
