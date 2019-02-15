# -*- coding: utf-8 -*-

from common.log import logger
import httplib2
import json
from conf.default import APP_ID, BK_PAAS_HOST
from django.http import HttpResponse, HttpResponseRedirect
from common.mymako import render_mako_context
from config import *


def get_uam_check_auth_url():
    return "{0}{1}".format(BK_PAAS_HOST + UAM_SITE_URL, 'check_auth')


def check_auth_from_server(user_id, func_code):
    try:
        http = httplib2.Http()
        body = {'user_id': user_id, 'func_code': func_code, 'app_id': APP_ID}
        headers = {'Content-type': 'application/json'}
        url = get_uam_check_auth_url()
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(body))
        return json.loads(content)['result']
    except Exception as e:
        logger.error('check_auth_from_server error : %s' % e)
        return False


def cw_check_auth(func_code):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if IS_USE_UAM_PERMISSION:
                _result = check_auth_from_server(request.user.username, func_code)
            else:
                _result = True
            if _result:
                # 成功
                return view_func(request, *args, **kwargs)
            else:
                if request.is_ajax():
                    return HttpResponse(status=403)
                return render_mako_context(request, '/403.html')
        return _wrapped_view
    return decorator
