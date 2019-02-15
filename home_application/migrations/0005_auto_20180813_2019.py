# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0004_auto_20180813_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMDBUsedIPs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='excludeips',
            name='ip_pool',
        ),
        migrations.RemoveField(
            model_name='usedips',
            name='ip_pool',
        ),
        migrations.RemoveField(
            model_name='ippools',
            name='used_count',
        ),
        migrations.AddField(
            model_name='ippools',
            name='assignable_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ips',
            name='is_assigned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ips',
            name='is_excluded',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ExcludeIPs',
        ),
        migrations.DeleteModel(
            name='UsedIPs',
        ),
    ]
