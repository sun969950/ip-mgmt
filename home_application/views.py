# -*- coding: utf-8 -*-

from common.mymako import render_mako_context
from home_application.apply_views import *
from home_application.sys_views import *
from home_application.ip_views import *
from home_application.home_views import *
from home_application.upload_cvs import *
from home_application.ip_manage import *
from home_application.operate_cvs import *
import sys
from home_application.ip_pool_view import *

reload(sys)
sys.setdefaultencoding("utf-8")


def home(request):
    """
    首页
    """
    # user = request.user
    # if not user.is_super_user:
    #     return render_mako_context(request, '/home_application/js_factory_user.html')
    # connection = pymysql.connect(**server_config)
    # cursor = connection.cursor()
    # sql = """select id  from bkaccount_bkuser where username='%s'""" % request.user.username
    # cursor.execute(sql)
    # result = cursor.fetchall()
    # connection.commit()
    # connection.close()
    # if result:
    #     user_id = result[0]["id"]
    # else:
    #     user_id = ""
    user_id = 2
    return render_mako_context(request, '/home_application/js_factory.html', {"user_id":user_id})


# def user(request):
#     """
#     首页
#     """
#     user_id = 2
#     return render_mako_context(request, '/home_application/js_factory_user.html', {"user_id": user_id})

