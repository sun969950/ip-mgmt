# -*- coding: utf-8 -*-

from common.mymako import render_json
from django.views.decorators.csrf import csrf_exempt
from account.views import login_exempt
import json
from home_application.celery_tasks import *
from conf.default import server_config
import pymysql
from IPy import IP
from django.db import transaction
from django.db.models import Q


def search_user_ips(request):
    try:
        filter_obj = eval(request.body)
        # ip_list = IPs.objects.filter(business__icontains=filter_obj["business"], owner=request.user.username)
        ip_list = IPs.objects.filter(business__icontains=filter_obj["business"],
                                     start_ip__icontains=filter_obj["ip"], owner=request.user.username)
        return_data = []
        for i in ip_list:
            return_data.append(i.to_dic())
        return render_json({"result": True, "data": return_data})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})

def search_used_ips(request):
    try:
        filter_obj = json.loads(request.body)
        if filter_obj['ip_pools']:
            ip_list = IPs.objects.filter(business__icontains=filter_obj["business"], start_ip__icontains=filter_obj["ip"],
                                     is_used=True,ip_pool_id=int(filter_obj['ip_pools']))
        else:
            ip_list = IPs.objects.filter(business__icontains=filter_obj["business"],
                                         start_ip__icontains=filter_obj["ip"],
                                         is_used=True)
        return_data = []
        for i in ip_list:
            return_data.append(i.to_dic())

        pool_list  = [{"id":i.id,"name":i.title+'('+i.ip_net+')'}for i in IPPools.objects.all()]

        return render_json({"result": True, "data": return_data,"pool_list":pool_list})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def search_ip_assigned_not_used(request):
    try:
        filter_obj = eval(request.body)
        # ip_list = IPs.objects.filter(business__icontains=filter_obj["business"], is_admin=False)
        # if filter_obj["ip"] == "":
        #     ip_list = IPs.objects.filter(is_assigned=True, is_used=False)
        # else:
        #     ip_list = IPs.objects.filter(start_ip=filter_obj["ip"], is_assigned=True, is_used=False)
        ip_list = IPs.objects.filter(business__icontains=filter_obj["business"],
                                     start_ip__icontains=filter_obj["ip"], is_assigned=True, is_used=False)
        return_data = []
        for i in ip_list:
            return_data.append(i.to_dic())
        return render_json({"result": True, "data": return_data})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def search_exclude_ips(request):
    try:
        filter_obj = json.loads(request.body)
        if filter_obj['ip_pools']:
            exclude_ips = IPs.objects.filter(start_ip__icontains=filter_obj["ip"],is_excluded=True,ip_pool_id=int(filter_obj['ip_pools']))
        else:
            exclude_ips = IPs.objects.filter(start_ip__icontains=filter_obj["ip"], is_excluded=True)

        pool_list = [{"id": i.id, "name": i.title + '(' + i.ip_net + ')'} for i in IPPools.objects.all()]
        return_data = []
        for i in exclude_ips:
            return_data.append(i.to_dic())
        return render_json({"result": True, "data": return_data,"pool_list":pool_list})
    except Exception,e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def search_usable_ips(request):
    try:
        filter_obj = json.loads(request.body)
        if filter_obj['ip_pools']:
            usable_ips = IPs.objects.filter(start_ip__icontains=filter_obj["ip"],
                                            is_used=False, is_excluded=False,ip_pool_id=int(filter_obj['ip_pools']))
        else:
            usable_ips = IPs.objects.filter(start_ip__icontains=filter_obj["ip"],is_used=False, is_excluded=False)
        return_data = []
        pool_list = [{"id": i.id, "name": i.title + '(' + i.ip_net + ')'} for i in IPPools.objects.all()]
        for i in usable_ips:
            return_data.append(i.to_dic())
        return render_json({"result": True, "data": return_data,"pool_list":pool_list})
    except Exception,e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


@login_exempt
def api_search_usable_ips(request):
    try:
        usable_ips = list(IPs.objects.filter(is_used=False, is_excluded=False).values_list("start_ip", flat=True))
        return render_json({"result": True, "data": usable_ips})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"获取可用IP失败，请联系管理员！"]})


@login_exempt
@csrf_exempt
def api_lock_usable_ip(request):
    try:
        req = json.loads(request.body)
        lock_ips = req["ip"]
        operator = req["operator"]
        for ip in lock_ips:
            ip_obj = IPs.objects.get(start_ip=ip)
            if ip_obj.is_excluded:
                return render_json({"result": False, "data": [u"锁定可用IP失败，请联系管理员！"]})
            else:
                ip_obj.is_excluded = True
                ip_obj.description = operator + "操作"
                ip_obj.save()
                insert_log(u"IP管理", operator, u"将IP标记为排除IP：IP--%s" % (ip))
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"锁定可用IP失败，请联系管理员！"]})


@login_exempt
@csrf_exempt
def api_unlock_ip(request):
    try:
        req = json.loads(request.body)
        lock_ips = req["ip"]
        operator = req["operator"]
        for ip in lock_ips:
            ip_obj = IPs.objects.get(start_ip=ip)
            if ip_obj.is_excluded:
                ip_obj.is_excluded = False
                ip_obj.description = ""
                ip_obj.save()
                insert_log(u"IP管理", operator, u"将IP移出排除IP：IP--%s" % (ip))
            else:
                return render_json({"result": False, "data": [u"IP未锁定，请联系管理员！"]})
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"解锁IP失败，请联系管理员！"]})


def create_ips(request):
    try:
        date_now_str = date_now()
        username = request.user.username
        ip_obj = json.loads(request.body)
        result = validate_ips(ip_obj["start_ip"], ip_obj["end_ip"])
        if not result["result"]:
            return render_json(result)
        # all_length = len(netaddr.IPRange(ip_obj["start_ip"], ip_obj["end_ip"]))
        ip_pool = IPPools.objects.get(id=ip_obj["ip_pool_id"])
        ip_pool_list = IP(ip_pool.ip_net)
        if not get_ip_exist(ip_pool_list, ip_obj):
            return render_json({"result": False, "data": [u"所选IP范围超出IP资源池"]})
        ip_query = IPs.objects.create(
            start_ip=ip_obj["start_ip"],
            end_ip=ip_obj["end_ip"],
            business=ip_obj["business"],
            # when_expired=ip_obj["when_expired"],
            owner=ip_obj["owner_name"],
            created_by=username,
            modified_by=username,
            when_modified=date_now_str,
            when_created=date_now_str,
            # is_admin=True,
            # all_length=all_length,
            # description=ip_obj["description"],
            ip_pool_id=ip_obj["ip_pool_id"]
        )
        # update_ip_used.delay(ip_pool)
        # get_ips_usage.delay(ip_query)
        insert_log(u"IP管理", request.user.username, u"新增网段：起始IP--%s，结束IP--%s" % (ip_query.start_ip, ip_query.end_ip))
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def modify_ips(request):
    try:
        date_now_str = date_now()
        username = request.user.username
        ip_obj = json.loads(request.body)
        result = validate_ips_exclude_self(ip_obj["start_ip"], ip_obj["end_ip"], ip_obj["id"])
        if not result["result"]:
            return render_json(result)
        ip_pool = IPPools.objects.get(id=ip_obj["ip_pool_id"])
        ip_pool_list = IP(ip_pool.ip_net)
        if not get_ip_exist(ip_pool_list, ip_obj):
            return render_json({"result": False, "data": [u"所选IP范围超出IP资源池"]})
        IPs.objects.filter(id=ip_obj["id"]).update(
            start_ip=ip_obj["start_ip"],
            end_ip=ip_obj["end_ip"],
            business=ip_obj["business"],
            # when_expired=ip_obj["when_expired"],
            modified_by=username,
            when_modified=date_now_str,
            # description=ip_obj["description"],
            owner=ip_obj["owner_name"]
        )
        # ip_query = IPs.objects.get(id=ip_obj["id"])
        # get_ips_usage.delay(ip_query)
        # update_ip_used.delay(ip_pool)
        insert_log(u"IP管理", request.user.username, u"修改网段：起始IP--%s，结束IP--%s" % (ip_query.start_ip, ip_query.end_ip))
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def delete_ips(request):
    try:
        ip_id = request.GET["id"]
        ip_obj = IPs.objects.get(id=ip_id)
        # ip_pool = ip_obj.ip_pool
        # start_ip = ip_obj.start_ip
        # end_ip = ip_obj.end_ip
        # update_ip_used.delay(ip_pool)
        ip_obj.owner = ""
        ip_obj.business = ""
        ip_obj.is_assigned = False
        ip_obj.when_modified = date_now()
        ip_obj.save()
        insert_log(u"IP管理", request.user.username, u"回收IP：IP--%s" % (ip_obj.start_ip))
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def detect_ips(request):
    try:
        ip_type = request.GET["ip_type"]
        if ip_type == "00":
            ips = request.GET["ips"]
            ip_list = ips.split(",")
            ip_result = one_ip_scan(ip_list)
        else:
            start_ip = request.GET["start_ip"]
            end_ip = request.GET["end_ip"]
            ip_result = IPNetScan(start_ip, end_ip)
        return render_json({"result": True, "data": [{"ip": i} for i in ip_result]})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def allocation_search(request):
    try:
        ip_type = request.GET["ip_type"]
        # ip_all = IPs.objects.all()
        # ip_allocation = []
        # ip_return = []
        # for i in ip_all:
        #     ip_pools = netaddr.IPRange(i.start_ip, i.end_ip)
        #     ip_tem_list = [str(u) for u in ip_pools]
        #     ip_allocation += ip_tem_list
        ip_used_or_exclude = set(IPs.objects.filter(Q(is_used=True) | Q(is_excluded=True)).values_list("start_ip",flat=True))
        # return_used_or_exclude = []
        # return_usable = []
        if ip_type == "00":
            ips = request.GET["ips"]
            ip_set = set(ips.split(","))
            ip_return = list(ip_set.intersection(ip_used_or_exclude))
        else:
            start_ip = request.GET["start_ip"]
            end_ip = request.GET["end_ip"]
            ip_net_pool = netaddr.IPRange(start_ip, end_ip)
            ip_net_set = set([str(ip) for ip in ip_net_pool])
            ip_return = list(ip_net_set.intersection(ip_used_or_exclude))
        return render_json({"result": True, "data": [{"ip": i} for i in ip_return]})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def get_all_user(request):
    try:
        connection = pymysql.connect(**server_config)
        cursor = connection.cursor()
        sql = """select id,username as text from bkaccount_bkuser"""
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return render_json({"result": True, "data": result})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def get_ip_exist(ip_pool_list, ip_obj):
    if ip_obj["start_ip"] not in ip_pool_list:
        return False
    if ip_obj["end_ip"] not in ip_pool_list:
        return False
    return True


def modify_ip(request):
    try:
        filter_obj = json.loads(request.body)
        IPs.objects.filter(id=filter_obj["id"]).update(business=filter_obj["business"],owner=filter_obj["owner"],description=filter_obj["description"])
        return render_json({"result": True})
    except Exception as e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})

def recycle_ip(request):
    try:
        filter_obj = json.loads(request.body)
        param = filter_obj['param']
        IPs.objects.filter(id=param['id']).update(is_used=False,owner='',business='',work_order='')
        insert_log(u"IP管理", request.user.username, u"回收ip：IP--%s" % (param["start_ip"]))
        return render_json({"result": True})
    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def delete_ip_exclude(request):
    try:
        filter_obj = json.loads(request.body)
        ip_obj = IPs.objects.get(id=filter_obj["id"])
        with transaction.atomic():
            ip_obj.is_excluded=False
            ip_obj.description=""
            ip_obj.save()
            ip_obj.ip_pool.all_count += 1
            ip_obj.ip_pool.assignable_count = ip_obj.ip_pool.ips_set.filter(is_used=False,is_excluded=False).count()
            ip_obj.ip_pool.save()
            # IPs.objects.filter(id=filter_obj["id"]).update(is_excluded=False, description="")
        insert_log(u"IP管理", request.user.username, u"将IP移出排除IP：IP--%s" % (filter_obj["start_ip"]))
        return render_json({"result": True})
    except Exception,e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def sync_cmdb(request):
    try:
        update_ip_used()
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})

