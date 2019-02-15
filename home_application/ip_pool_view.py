# -*-encoding=utf-8 -*-

from common.mymako import render_json
from IPy import IP
from home_application.models import IPPools, IPs
import json
from common.log import logger
import netaddr
from home_application.helper_view import insert_log,date_now
from django.db import transaction
from django.db.models import Q
import struct
import socket


def findIPs(start, end):
    if start and end:
        ipstruct = struct.Struct('>I')
        start, = ipstruct.unpack(socket.inet_aton(start))
        end, = ipstruct.unpack(socket.inet_aton(end))
        return [socket.inet_ntoa(ipstruct.pack(i)) for i in range(start, end + 1)]
    else:
        return []

SYS_ERROR = {"result": False, "data": ["系统异常，请联系管理员！"]}


def get_is_ip_overlaps(ip_net, ip_pool_id=None):
    net_list = IPPools.objects.exclude(id=ip_pool_id).values("ip_net")
    for i in net_list:
        if IP(ip_net).overlaps(i["ip_net"]):
            return True
    return False


def get_has_ip_used(ip_pool_obj):
    ip_list = IPs.objects.filter(ip_pool_id=ip_pool_obj["id"], is_used=True)
    # ip_used_list = []
    # for i in ip_list:Ｔｒｕｅ
    #     ip_range = netaddr.IPRange(i.start_ip, i.end_ip)
    #     ip_used_list += [str(u) for u in ip_range]
    # for i in set(ip_list):
    #     if i not in IP(ip_pool_obj["ip_net"]):
    #         return True
    if len(ip_list) > 0:
        return True
    else:
        return False


def create_ip_pool(request):
    try:
        obj = json.loads(request.body)
        obj["created_by"] = request.user.username
        if IPPools.objects.filter(title=obj['title']):
            return render_json({'result': False, 'data': [u'资源池已存在，请检查确认！']})

        when_created = date_now()
        count = 0
        ip_range = []
        excute_range = []
        add_ip = []
        excute_list = []

        if len(obj['excute_range']):
            for excute in obj['excute_range']:
                excute_range.append(excute['ip_start']+'-'+excute['ip_end'])
                excute_ips = findIPs(excute['ip_start'],excute['ip_end'])
                excute_list+=excute_ips

        exclude_ip_list = list(set(excute_list))

        for interval in obj["interval_list"]:
            ip_range.append(interval["ip_start"] + '-' + interval["ip_end"])
            ipArr = findIPs(interval['ip_start'], interval['ip_end'])
            count += len(ipArr)
            add_ip += ipArr

        add_ip = list(set(add_ip))

        if get_is_ip_overlaps(obj["ip_net"]):
            return render_json({"result": False, "data": [u"存在重叠IP"]})
        for ip in exclude_ip_list:
            if ip not in add_ip:
                return render_json({"result": False, "data": [u"要排除的IP不在网段范围内"]})

        ips = IP(obj["ip_net"])
        obj["ip_start"] = str(ips[0])
        obj["ip_end"] = str(ips[-1])
        ip_range = ",".join(ip_range)
        obj["range"] = ip_range
        obj["all_count"] = count - len(exclude_ip_list)
        obj["assignable_count"] = obj["all_count"]
        obj['excute_range'] = ','.join(excute_range)
        obj['use_rate'] = 100
        ip_pool = IPPools()
        with transaction.atomic():
            ip_pool.create_item(obj)
            ip_pool_ins = IPPools.objects.get(ip_net=obj["ip_net"])
            list_to_create = []
            for i in add_ip:
                if i in exclude_ip_list:
                    list_to_create.append(
                        IPs(start_ip=i, end_ip=i, ip_pool=ip_pool_ins, created_by=obj["created_by"],
                            when_created=when_created, is_excluded=True,mask=obj['mask'],gateway=obj['gateway']))
                else:
                    list_to_create.append(
                        IPs(start_ip=i, end_ip=i, ip_pool=ip_pool_ins, created_by=obj["created_by"],
                            when_created=when_created,mask=obj['mask'],gateway=obj['gateway']))
            IPs.objects.bulk_create(list_to_create)
        insert_log(u"资源池管理", request.user.username, u"新增资源池：%s" % ip_pool.title + ": " + ip_pool.ip_net)
        for ip in exclude_ip_list:
            insert_log(u"IP管理", request.user.username, u"将IP标记为排除IP：IP--%s" % ip)
        return render_json({"result": True, "data": ip_pool.to_dic()})

    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [e]})


def create_pool(obj, username):
    try:
        when_created = date_now()
        exclude_ip_list = set([i["ip"] for i in obj["exclude_ip_list"] if i["ip"]])
        if get_is_ip_overlaps(obj["ip_net"]):
            return render_json({"result": False, "data": [u"存在重叠IP"]})
        for ip in exclude_ip_list:
            if IP(obj["ip_net"]).overlaps(ip) != 1:
                return render_json({"result": False, "data": [u"要排除的IP不在网段范围内"]})
        obj["all_count"] = IP(obj["ip_net"]).len() - len(exclude_ip_list)
        obj["assignable_count"] = obj["all_count"]
        ips = IP(obj["ip_net"])
        obj["ip_start"] = str(ips[0])
        obj["ip_end"] = str(ips[-1])
        obj["range"] = ""
        ip_pool = IPPools()
        with transaction.atomic():
            ip_pool.create_item(obj)
            ip_pool_ins = IPPools.objects.get(ip_net=obj["ip_net"])
            ip_pool_range = netaddr.IPRange(ip_pool_ins.ip_start, ip_pool_ins.ip_end)
            ip_list = [str(u) for u in ip_pool_range]
            list_to_create = []
            for i in ip_list:
                if i in exclude_ip_list:
                    list_to_create.append(IPs(start_ip=i, end_ip=i, ip_pool=ip_pool_ins, created_by=obj["created_by"],
                                              when_created=when_created, is_excluded=True))
                else:
                    list_to_create.append(IPs(start_ip=i, end_ip=i, ip_pool=ip_pool_ins, created_by=obj["created_by"],
                                              when_created=when_created))
            IPs.objects.bulk_create(list_to_create)
            insert_log(u"资源池管理", username, u"新增资源池：%s" % ip_pool.title + ": " + ip_pool.ip_net)
            for ip in exclude_ip_list:
                insert_log(u"IP管理", username, u"将IP标记为排除IP：IP--%s" % ip)
            return render_json({"result": True, "data": ip_pool.to_dic()})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"网段格式有误"]})


def modify_ip_pool(request):
    try:
        obj = json.loads(request.body)
        obj["modified_by"] = request.user.username
        pool_name = IPPools.objects.filter(title=obj["title"]).exclude(id=obj["id"])
        if pool_name:
            return render_json({'result': True, 'data': [u'资源池已存在']})

        # exclude_ip_list = set([i["ip"] for i in obj["exclude_ip_list"] if i["ip"]])
        ip_pool = IPPools.objects.get(id=obj["id"])
        when_created = date_now()
        count = 0
        new_ip = []
        excute_range = []
        excute_list = []
        for excute in obj['excute_range']:
            excute_range.append(excute['ip_start']+'-'+excute['ip_end'])
            excute_ips = findIPs(excute['ip_start'],excute['ip_end'])
            excute_list+=excute_ips

        exclude_ip_list = list(set(excute_list))
        ip_range = []
        add_ip = []
        for interval in obj["interval_list"]:
            ip_range.append(interval["ip_start"] + '-' + interval["ip_end"])
            ipArr = findIPs(interval['ip_start'], interval['ip_end'])
            count += len(ipArr)
            add_ip += ipArr
            if interval['status'] == 'new':
                new_ip += ipArr

        new_ip = list(set(new_ip))
        add_ip = list(set(add_ip))
        for ip in exclude_ip_list:
            if ip not in add_ip:
                return render_json({"result": False, "data": [u"要排除的IP不在网段范围内"]})
        ip_range = ",".join(ip_range)
        obj["range"] = ip_range
        obj['excute_range'] = ','.join(excute_range)

        # used_ip_list = []
        # if get_is_ip_overlaps(obj["ip_net"], obj["id"]):
        #     return render_json({"result": False, "data": [u"存在重叠IP"]})
        # if get_has_ip_used(obj) and ip_pool.ip_net != obj["ip_net"]:
        #     return render_json({"result": False, "data": [u"部分IP已被使用，无法修改网段"]})
        # for ip in exclude_ip_list:
        #     if IP(obj["ip_net"]).overlaps(ip) != 1:
        #         return render_json({"result": False, "data": [u"要排除的IP不在网段范围内"]})
        # else:
        #     used_or_assigned_list = ip_pool.ips_set.filter(Q(is_used=True) | Q(is_assigned=True)).values_list("start_ip", flat=True)
        #     if ip in used_or_assigned_list:
        #         return render_json({"result": False, "data": [u"要排除的IP已被分配或使用"]})
        obj["all_count"] = len(add_ip) - len(exclude_ip_list)
        ips = IP(obj["ip_net"])
        obj["ip_start"] = str(ips[0])
        obj["ip_end"] = str(ips[-1])
        with transaction.atomic():
            ip_pool.create_item(obj)
            ip_pool_ins = IPPools.objects.get(ip_net=obj["ip_net"])
            list_to_create = []
            for i in new_ip:
                if i in exclude_ip_list:
                    list_to_create.append(
                        IPs(start_ip=i, end_ip=i, ip_pool=ip_pool_ins, created_by=obj["created_by"],
                            when_created=when_created, is_excluded=True,mask=obj['mask'],gateway=obj['gateway']))
                else:
                    list_to_create.append(
                        IPs(start_ip=i, end_ip=i, ip_pool=ip_pool_ins, created_by=obj["created_by"],
                            when_created=when_created,mask=obj['mask'],gateway=obj['gateway']))
            IPs.objects.bulk_create(list_to_create)

            ip_pool.modify_item(obj)
            insert_log(u"资源池管理", request.user.username, u"修改资源池：%s" % ip_pool.title + ": " + ip_pool.ip_net)
            old_exclude_ips =set([str(i) for i in ip_pool.ips_set.filter(is_excluded=True).values_list("start_ip", flat=True)])
            new_exclude_ips = set(exclude_ip_list)
            update_exclude_true = new_exclude_ips - old_exclude_ips
            update_exclude_false = old_exclude_ips - new_exclude_ips
            for ip in update_exclude_true:
                IPs.objects.filter(start_ip=ip).update(is_excluded=True)
                insert_log(u"IP管理", request.user.username, u"将IP标记为排除IP：IP--%s" % ip)
            for ip in update_exclude_false:
                IPs.objects.filter(start_ip=ip).update(is_excluded=False)
                insert_log(u"IP管理", request.user.username, u"将IP移出排除IP：IP--%s" % ip)
            ip_pool.assignable_count = IPs.objects.filter(ip_pool=obj["id"], is_used=False, is_excluded=False).count()
            ip_pool.save()
            # ExcludeIPs.objects.bulk_create([ExcludeIPs(ip=i, ip_pool=ip_pool) for i in exclude_ip_list])
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json(SYS_ERROR)


def delete_ip_pool(request):
    try:
        obj = json.loads(request.body)
        # if get_has_ip_used(obj):
        #     return render_json({"result": False, "data": [u"部分IP已被分配未使用，无法删除"]})
        IPPools.objects.filter(id=obj["id"]).delete()
        insert_log(u"资源池管理", request.user.username, u"删除资源池：%s" % obj["title"] + ": " + obj["ip_net"])
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json(SYS_ERROR)


def get_ip_pools(request):
    try:
        pool_list = IPPools.objects.all()
        return render_json(
            {"result": True, "data": [{"id": i.id, "text": i.title + "(" + i.ip_net + ")"} for i in pool_list]})
    except Exception, e:
        logger.exception(e)
        return render_json(SYS_ERROR)


def search_ip_pools(request):
    try:
        filter_obj = eval(request.body)
        pools = IPPools.objects.filter(
            title__icontains=filter_obj["title"],
            ip_net__icontains=filter_obj['ip_net']
        )
        pool_list = []
        # pool_list = IPPools.objects.filter(title__icontains=filter_obj["title"]).values()
        for pool in pools:
            res = pool.to_dic()
            all_count = len(IPs.objects.filter(ip_pool_id=res['id']))
            res['all_count'] = all_count
            res['threshold'] = int(res['threshold'])
            res['ip_range'] = res['range']

            used_ips = IPs.objects.filter(ip_pool_id=res['id'],is_used=1)
            a = len(used_ips)
            res['assignable_count'] = len(IPs.objects.filter(ip_pool_id=res['id'],is_used=0))

            rate = '%.2f' %(len(used_ips)*100/float(res['all_count']))
            res['use_rate'] = rate
            ip_range = []
            excute_ip = []
            if res['range']:
                range_arr = res['range'].split(",")
                for i in range(0, len(range_arr)):
                    temp = {}
                    temp['ip_start'] = range_arr[i].split("-")[0]
                    temp['ip_end'] = range_arr[i].split("-")[1]
                    temp['index'] = i + 1
                    temp['status'] = 'old'
                    ip_range.append(temp)
                res['range'] = ip_range
            else:
                ip_range.append({"index": 1, "ip_start": "", "ip_end": ""})
                res['range'] = ip_range

            if res['excute_range']:
                range_arr = res['excute_range'].split(",")
                for i in range(0, len(range_arr)):
                    temp = {}
                    temp['ip_start'] = range_arr[i].split("-")[0]
                    temp['ip_end'] = range_arr[i].split("-")[1]
                    temp['index'] = i + 1
                    excute_ip.append(temp)
                res['excute_range'] = excute_ip
            else:
                excute_ip.append({"index": 1, "ip_start": "", "ip_end": ""})
                res['excute_range'] = excute_ip

            # exclude_ip_list = [ip for ip in pool.ips_set.filter(is_excluded=True).values_list("start_ip", flat=True)]
            # if len(exclude_ip_list) == 0:
            #     res["exclude_ip_list"] = [{"index": 1, "ip": ""}]
            # else:
            #     res["exclude_ip_list"] = []
            #     for i in range(0, len(exclude_ip_list)):
            #         res["exclude_ip_list"].append({"index": i + 1, "ip": exclude_ip_list[i]})
            pool_list.append(res)
        return render_json({"result": True, "data": pool_list})
    except Exception, e:
        logger.exception(e)
        return render_json(SYS_ERROR)
