# -*-encoding=utf-8 -*-
from common.log import logger
from common.mymako import render_json
from home_application.models import *
import datetime


def get_count_obj(request):
    try:
        change_list, categories = set_log_chart()
        # ips = IPs.objects.all()
        # apply_length = Apply.objects.all().count()
        usable_ips = IPs.objects.filter(is_used=False, is_excluded=False).count()
        used_ips = IPs.objects.filter(is_used=True).count()
        excluded_not_used_ips = IPs.objects.filter(is_used=False, is_excluded=True).count()
        excluded_ips = IPs.objects.filter(is_excluded=True).count()
        # net_ips = len(ips)
        # for i in ips:
        #     usable_ips += i.all_length
        #     used_ips += i.used_num
        all_ips = 0
        ip_pools = IPPools.objects.all().values("all_count")
        net_ips = len(ip_pools)
        for i in ip_pools:
            all_ips += i["all_count"]
        # assignable_ips = IPs.objects.filter(is_used=False, is_excluded=False).count()
        user_ip_list = [
            {"name": u"已用的IP数", "y": used_ips, "color": "#f7a35c"},
            {"name": u"已排除未使用的IP数", "y": excluded_not_used_ips, "color": "#90ed7d"},
            {"name": u"可用的IP数", "y": usable_ips, "color":"#7cb5ec"},
        ]
        return render_json({
            "result": True,
            "data": {"usableIPs": usable_ips, "usedIps": used_ips, "excludedIPs": excluded_ips, "netIps": net_ips},
            "change_list": change_list,
            "userIpList": user_ip_list,
            "categories": categories
        })
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def set_apply_chart():
    dateNow = datetime.datetime.now()
    dateStart = dateNow + datetime.timedelta(days=-9)
    return_data = [{"name": u"申请单数", "data": []}]
    categories = []
    for i in xrange(10):
        dateBegin = dateStart + datetime.timedelta(days=i)
        date_start = str(dateBegin.date()) + " 00:00:00"
        date_end = str(dateBegin.date()) + " 23:59:59"
        applies = Apply.objects.filter(when_created__range=(date_start, date_end)).count()
        return_data[0]["data"].append(applies)
        categories.append(str(dateBegin.date()).split("-")[1] + "-" + str(dateBegin.date()).split("-")[2])
    return return_data, categories


def set_log_chart():
    dateNow = datetime.datetime.now()
    dateStart = dateNow + datetime.timedelta(days=-9)
    return_data = [{"name": u"变动IP数", "data": []}]
    categories = []
    for i in xrange(10):
        dateBegin = dateStart + datetime.timedelta(days=i)
        date_start = str(dateBegin.date()) + " 00:00:00"
        date_end = str(dateBegin.date()) + " 23:59:59"
        ip_changes = Logs.objects.filter(when_created__range=(date_start, date_end), operated_type='IP管理').count()
        return_data[0]["data"].append(ip_changes)
        categories.append(str(dateBegin.date()).split("-")[1] + "-" + str(dateBegin.date()).split("-")[2])
    return return_data, categories
