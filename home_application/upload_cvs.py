# -*-coding:utf-8-*-
from home_application.models import IPPools, IPs
from common.mymako import render_json
from common.log import logger
from IPy import IP
from django.db import transaction
import netaddr
from home_application.helper_view import insert_log
from home_application.ip_pool_view import findIPs

from django.http import HttpResponse
from account.decorators import login_exempt
from conf.default import PROJECT_ROOT
from django.db.models import Q
import json
import datetime
import os
import StringIO
import csv, codecs


def str_now_date():
    return str(datetime.datetime.now()).split(".")[0]


def upload_ippools(request):
    try:
        up_data = json.loads(request.body)
        for obj in up_data:
            obj["created_by"] = request.user.username
            when_created = str_now_date()
            if get_is_ip_overlaps(obj["ip_net"]):
                return render_json({"result": False, "data": [u"存在重叠IP"]})

            add_ip = []
            ip_range = []
            for interval in obj['range'].split(' '):
                ip_range.append(interval)
                ran = interval.split('-')
                ipArr = findIPs(ran[0], ran[1])
                add_ip += ipArr

            add_ip = list(set(add_ip))

            obj["all_count"] = len(add_ip)
            obj["assignable_count"] = obj["all_count"]
            ips = IP(obj["ip_net"])
            obj["ip_start"] = str(ips[0])
            obj["ip_end"] = str(ips[-1])
            obj['range'] = ','.join(ip_range)
            ip_pool = IPPools()
            with transaction.atomic():
                ip_pool.create_item(obj)
                ip_pool_ins = IPPools.objects.get(ip_net=obj["ip_net"])
                ip_pool_range = netaddr.IPRange(ip_pool_ins.ip_start, ip_pool_ins.ip_end)
                ip_list = add_ip
                list_to_create = []
                for i in ip_list:
                    list_to_create.append(IPs(start_ip=i, end_ip=i, ip_pool=ip_pool_ins, created_by=obj["created_by"],
                                              when_created=when_created, mask=obj['mask'], gateway=obj['gateway']))
                IPs.objects.bulk_create(list_to_create)
            insert_log(u"资源池管理", request.user.username, u"新增资源池：%s" % ip_pool.title + ": " + ip_pool.ip_net)
        return render_json({"result": True, "data": ip_pool.to_dic()})
    except Exception as e:
        logger.exception('upload cvs error:{0}'.format(e.message))
        return render_json({'result': False, 'msg': '上传失败'})


def get_is_ip_overlaps(ip_net, ip_pool_id=None):
    net_list = IPPools.objects.exclude(id=ip_pool_id).values("ip_net")
    for i in net_list:
        if IP(ip_net).overlaps(i["ip_net"]):
            return True
    return False
