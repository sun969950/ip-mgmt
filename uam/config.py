# -*- coding: utf-8 -*-
import os


IS_USE_UAM_PERMISSION = True
UAM_APP_ID = 'uam'
env = os.environ.get('BK_ENV', 'development')
if env.endswith('production'):
    UAM_SITE_URL = '/o/%s/' % UAM_APP_ID
else:
    UAM_SITE_URL = '/t/%s/' % UAM_APP_ID
