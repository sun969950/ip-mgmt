# -*- coding: utf-8 -*-

from common.log import logger
import httplib2
import json
from conf.default import APP_ID, BK_PAAS_HOST, APP_TOKEN
from django.http import HttpResponseRedirect
from config import *


# helpers


def get_uam_check_access_permission_url():
    return "{0}{1}".format(BK_PAAS_HOST + UAM_SITE_URL, 'check_access_permission')


def get_uam_no_permission_url():
    return "{0}{1}".format(BK_PAAS_HOST + UAM_SITE_URL, 'error_403')


def get_all_code_has_permission_url():
    return "{0}{1}".format(BK_PAAS_HOST + UAM_SITE_URL, 'get_all_code_has_permission')


def get_all_configs_url():
    return "{0}{1}".format(BK_PAAS_HOST + UAM_SITE_URL, 'get_all_config')


def get_config_value_url():
    return "{0}{1}".format(BK_PAAS_HOST + UAM_SITE_URL, 'get_config_value')


# ********************** #


# public
def check_login_auth_from_server(user_id):
    try:
        http = httplib2.Http()
        body = {'user_id': user_id, 'app_id': APP_ID}
        headers = {'Content-type': 'application/json'}
        url = get_uam_check_access_permission_url()
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(body))
        dic = json.loads(content)
        return dic['result'], dic['is_super_user']
    except Exception as e:
        logger.error('check_login_auth_from_server error : %s' % e)
        return False


def check_is_super_user(user_id):
    try:
        http = httplib2.Http()
        body = {'user_id': user_id, 'app_id': APP_ID}
        headers = {'Content-type': 'application/json'}
        url = get_uam_check_access_permission_url()
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(body))
        dic = json.loads(content)
        return {"result": dic['result'], "is_super_user": dic['is_super_user']}
    except Exception as e:
        logger.error('check_login_auth_from_server error : %s' % e)
        return {"result": False, "error": e.message if e.message else str(e)}


def redirect_to_403():
    tem = get_uam_no_permission_url()
    return HttpResponseRedirect(tem)


def get_all_code_has_permission(user_id):
    try:
        http = httplib2.Http()
        body = {'user_id': user_id, 'app_id': APP_ID}
        headers = {'Content-type': 'application/json'}
        url = get_all_code_has_permission_url()
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(body))
        dic = json.loads(content)
        return dic['data']
    except Exception as e:
        logger.error('check_login_auth_from_server error : %s' % e)
        return []


# 获取指定配置项字典
def get_all_configs():
    try:
        http = httplib2.Http()
        body = {'app_id': APP_ID, 'app_token': APP_TOKEN}
        headers = {'Content-type': 'application/json'}
        url = get_all_configs_url()
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(body))
        dic = json.loads(content)
        return dic['data']
    except Exception as e:
        logger.error('get_all_configs error : %s' % e)
        return {}


# 获取指定配置项的值
def get_config_value(code):
    try:
        http = httplib2.Http()
        body = {'code': code, 'app_id': APP_ID, 'app_token': APP_TOKEN}
        headers = {'Content-type': 'application/json'}
        url = get_config_value_url()
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(body))
        dic = json.loads(content)
        return dic['data']
    except Exception as e:
        logger.error('get_config_value error : %s' % e)
        return ''
