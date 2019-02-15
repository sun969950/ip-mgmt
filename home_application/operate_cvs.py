# -*- coding: utf-8 -*-
from home_application.models import IPs
from common.mymako import render_json
from common.log import logger
from home_application.helper_view import insert_log
from django.http import HttpResponse
from account.decorators import login_exempt
from conf.default import PROJECT_ROOT
import os
import csv, codecs
import json


# 导出cvs文件
def download_file(file_path, file_name):
    try:
        file_path = file_path
        file_buffer = open(file_path, 'rb').read()
        response = HttpResponse(file_buffer, content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        response['Content-Length'] = os.path.getsize(file_path)
        return response
    except Exception as e:
        logger.exception("download file error:{0}".format(e.message))
        return False


def down_exclude_ips(request):
    try:
        ip = request.GET.get('ip')
        ip_pool = request.GET.get('ip_pools')
        if ip_pool:
            cvs_data = list(IPs.objects.filter(is_excluded=True, start_ip__icontains=ip, ip_pool_id=ip_pool))
        else:
            cvs_data = list(IPs.objects.filter(is_excluded=True, start_ip__icontains=ip))

        cvs_data = [{
                        'id': i.id,
                        'start_ip': i.start_ip,
                        'pool': i.ip_pool.title + '(' + i.ip_pool.ip_net + ')',
                        'description': i.description,
                        'when_created': i.when_created} for i in cvs_data]

        data_list = []
        for i in cvs_data:
            data_list.append(
                [i['start_ip'], i['pool'], i['when_created'], i['description']]
            )
        f = codecs.open('IP.csv', 'wb', "gbk")
        writer = csv.writer(f)
        writer.writerow(["ip", "所属资源池", "创建时间", "备注"])
        writer.writerows(data_list)

        f.close()
        file_path = "{0}/IP.csv".format(PROJECT_ROOT).replace("\\", "/")
        file_name = "IP.csv"
        return download_file(file_path, file_name)
    except Exception as e:
        logger.exception('download cvs file error:{0}'.format(e.message))
        return False


def down_used_ips(request):
    try:
        ip = request.GET.get('ip')
        ip_pool = request.GET.get('ip_pools')
        business = request.GET.get('business')
        owner = request.GET.get('admin')
        work_order = request.GET.get('work_order')
        if ip_pool:
            cvs_data = list(IPs.objects.filter(is_used=True, business__contains=business, start_ip__icontains=ip,
                                               ip_pool_id=ip_pool, owner__contains=owner,
                                               work_order__contains=work_order))
        else:
            cvs_data = list(IPs.objects.filter(is_used=True, start_ip__icontains=ip, business__contains=business,
                                               owner__contains=owner, work_order__contains=work_order))

        cvs_data = [{
                        'id': i.id,
                        'pool': i.ip_pool.title + '(' + i.ip_pool.ip_net + ')',
                        'start_ip': i.start_ip,
                        'mask': i.mask,
                        'gateway': i.gateway,
                        'is_used': "已使用" if not i.is_used else "未使用",
                        'business': i.business,
                        'owner': i.owner,
                        'work_order': i.work_order
                    } for i in cvs_data]

        data_list = []
        for i in cvs_data:
            data_list.append(
                [i['pool'], i['start_ip'], i['mask'], i['gateway'], i['is_used'], i['business'], i['owner'],
                 i['work_order']]
            )
        f = codecs.open('usedIp.csv', 'wb', "gbk")
        writer = csv.writer(f)
        writer.writerow(["所属资源池", "ip", "掩码", "网关", "状态", "业务系统", "管理员", "工单号"])
        writer.writerows(data_list)

        f.close()
        file_path = "{0}/usedIp.csv".format(PROJECT_ROOT).replace("\\", "/")
        file_name = "usedIp.csv"
        return download_file(file_path, file_name)
    except Exception as e:
        logger.exception('download cvs file error:{0}'.format(e.message))
        return False


def down_useable_ips(request):
    try:
        ip = request.GET.get('ip')
        ip_pool = request.GET.get('ip_pools')
        if ip_pool:
            cvs_data = list(
                IPs.objects.filter(is_used=False, is_excluded=False, start_ip__icontains=ip, ip_pool_id=ip_pool))
        else:
            cvs_data = list(IPs.objects.filter(is_used=False, is_excluded=False, start_ip__icontains=ip))

        cvs_data = [{
                        'id': i.id,
                        'pool': i.ip_pool.title + '(' + i.ip_pool.ip_net + ')',
                        'start_ip': i.start_ip,
                        'mask': i.mask,
                        'gateway': i.gateway,
                        'is_used': "未使用" if not i.is_used else "已使用", } for i in cvs_data]

        data_list = []
        for i in cvs_data:
            data_list.append(
                [i['pool'], i['start_ip'], i['mask'], i['gateway'], i['is_used']]
            )
        f = codecs.open('can_use.csv', 'wb', "gbk")
        writer = csv.writer(f)
        writer.writerow(["资源池", "ip", "掩码", "网关", "状态"])
        writer.writerows(data_list)

        f.close()
        file_path = "{0}/can_use.csv".format(PROJECT_ROOT).replace("\\", "/")
        file_name = "can_use.csv"
        return download_file(file_path, file_name)
    except Exception as e:
        logger.exception('download cvs file error:{0}'.format(e.message))
        return False


def upload_usedIps(request):
    try:
        up_data = json.loads(request.body)
        fail_ips = []
        for up in up_data:
            is_in = IPs.objects.filter(start_ip=up['ip'])
            if is_in:
                IPs.objects.filter(start_ip=up['ip']).update(
                    mask=up['mask'],
                    gateway=up['gateway'],
                    is_used=int(up['is_used']),
                    business=up['business'],
                    owner=up['owner'],
                    work_order=up['work_order']
                )
            else:
                fail_ips.append(up['ip'])
        if fail_ips:
            insert_log(u"IP管理", request.user.username, u"已用ip导入 {0}导入失败，无对应资源池".format(fail_ips))
            return render_json({'result': True, 'data': fail_ips, 'part': True})
        else:
            insert_log(u"IP管理", request.user.username, u"已用ip导入成功")
            return render_json({'result': True, 'data': [u'上传成功！'], 'part': False})

    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def down_template(request):
    try:
        cvs_data = [{
                        'pool': "资源池1",
                        'business': "蓝鲸",
                        'owner': "小张",
                        'work_order':"12345678"
        }]
        data_list = []
        for i in cvs_data:
            data_list.append(
                [i['pool'], i['business'], i['owner'], i['work_order']]
            )
        f = codecs.open('template.csv', 'wb', "gbk")
        writer = csv.writer(f)
        writer.writerow(["资源池", "业务系统", "管理员", "工单号"])
        writer.writerows(data_list)

        f.close()
        file_path = "{0}/template.csv".format(PROJECT_ROOT).replace("\\", "/")
        file_name = "template.csv"
        return download_file(file_path, file_name)
    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})
