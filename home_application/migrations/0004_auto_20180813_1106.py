# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_excludeips'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsedIPs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=15)),
                ('ip_pool', models.ForeignKey(to='home_application.IPPools')),
            ],
        ),
        migrations.RemoveField(
            model_name='ips',
            name='all_length',
        ),
        migrations.RemoveField(
            model_name='ips',
            name='description',
        ),
        migrations.RemoveField(
            model_name='ips',
            name='ip_used_list',
        ),
        migrations.RemoveField(
            model_name='ips',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='ips',
            name='is_expired',
        ),
        migrations.RemoveField(
            model_name='ips',
            name='used_num',
        ),
        migrations.RemoveField(
            model_name='ips',
            name='when_expired',
        ),
        migrations.AddField(
            model_name='ips',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
