# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from settings import SETTINGS_JSON_FILE
from home_application.models import *
import datetime


def initial_settings_data(apps, schema_editor):
    try:
        Settings.objects.all().delete()
        json_data = open(SETTINGS_JSON_FILE)
        settings_check_item_obj = json.load(json_data)
        for i in settings_check_item_obj:
            Settings.objects.create(id=i['id'], key=i['key'], value=i['value'],
                                    description=i['description'])
        json_data.close()
    except Exception, e:
        return e.message


class Migration(migrations.Migration):
    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_settings_data),
    ]
