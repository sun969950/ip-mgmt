# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apply_num', models.CharField(max_length=20)),
                ('when_created', models.CharField(max_length=20)),
                ('when_expired', models.CharField(max_length=20)),
                ('ip_list', models.TextField()),
                ('ip_type', models.CharField(max_length=10)),
                ('created_by', models.CharField(max_length=100)),
                ('business', models.CharField(max_length=200)),
                ('approved_by', models.CharField(default=b'', max_length=100, null=True)),
                ('when_approved', models.CharField(default=b'', max_length=20, null=True)),
                ('apply_reason', models.CharField(max_length=200)),
                ('refuse_reason', models.CharField(default=b'', max_length=200, null=True)),
                ('description', models.CharField(default=b'', max_length=200, null=True)),
                ('status', models.CharField(default=b'00', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='IPPools',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_start', models.CharField(max_length=50)),
                ('ip_end', models.CharField(max_length=50)),
                ('when_created', models.CharField(max_length=30)),
                ('when_modified', models.CharField(default=b'', max_length=30)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_by', models.CharField(default=b'', max_length=100)),
                ('ip_net', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('all_count', models.IntegerField()),
                ('used_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IPs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_ip', models.CharField(max_length=20)),
                ('end_ip', models.CharField(max_length=20)),
                ('business', models.CharField(default=b'', max_length=100, null=True)),
                ('when_expired', models.CharField(max_length=20)),
                ('owner', models.CharField(max_length=100)),
                ('is_expired', models.BooleanField(default=False)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_by', models.CharField(max_length=100)),
                ('when_modified', models.CharField(max_length=100)),
                ('when_created', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField(default=False)),
                ('used_num', models.IntegerField(default=0)),
                ('all_length', models.IntegerField(default=0)),
                ('ip_used_list', models.TextField(default=b'', null=True)),
                ('description', models.CharField(default=b'', max_length=200, null=True)),
                ('ip_pool', models.ForeignKey(to='home_application.IPPools')),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operated_type', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('when_created', models.CharField(max_length=30)),
                ('operator', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Mailboxes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('mailbox', models.CharField(max_length=100)),
                ('when_created', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=50)),
                ('value', models.TextField()),
                ('description', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='apply',
            name='ip_pool',
            field=models.ForeignKey(to='home_application.IPPools'),
        ),
    ]
