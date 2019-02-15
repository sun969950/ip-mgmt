# -*-encoding=utf-8 -*-

from home_application.models import IPs, IPPools
from common.log import logger
from home_application.helper_view import insert_log, date_now
from common.mymako import render_json
from django.views.decorators.csrf import csrf_exempt
from account.views import login_exempt
import random
import json


def allocate_ip(request):
    try:
        allocate_data = json.loads(request.body)
        logger.error(allocate_data)
        avail_ips = [
            {
                'id': i.id,
                'ip': i.start_ip
            } for i in IPs.objects.filter(is_used=0, is_excluded=0, ip_pool_id=int(allocate_data['ipPool']))
        ]
        is_in = IPs.objects.filter(ip_pool_id=allocate_data['ipPool'], business=allocate_data['sys'],
                                   owner=allocate_data['admin'],
                                   work_order=allocate_data['workOrder'])
        pool_title = IPPools.objects.get(id=allocate_data['ipPool']).title
        if is_in:
            insert_log(u"手动分配IP失败", request.user.username,
                       "{0}/{1}/{2}/{3} 已有分配IP".format(pool_title, allocate_data['sys'],
                                                       allocate_data['admin'],
                                                       allocate_data['workOrder']))
            return render_json({"result": False, "message": '已分配，请勿重复分配！'})
        if not len(avail_ips):
            insert_log(u"手动分配IP失败", request.user.username, "{0} 资源池 已无可分配ip".format(pool_title))
            return render_json({"result": False, "message": '已无可分配ip'})

        random_ip = avail_ips[random.randint(0, (len(avail_ips))-1)]

        IPs.objects.filter(id=random_ip['id']).update(
            business=allocate_data['sys'],
            owner=allocate_data['admin'],
            when_modified=date_now(),
            is_used=1,
            work_order=allocate_data['workOrder']
        )

        insert_log(u"手动分配IP", request.user.username,
                   "{0}/{1}/{2}/{3} => 分配 ip : {4}".format(pool_title, allocate_data['sys'], allocate_data['admin'],
                                                           allocate_data['workOrder'], random_ip['ip']))
        return render_json({"result": True, "data": {'random_ip': random_ip['ip']}})

    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "data": [u"系统异常，请联系管理员"]})


# 后期需要修改
def get_relate_data(request):
    try:
        ip_pools = [{'id': i.id, 'name': i.title + '(' + i.ip_net + ')'} for i in IPPools.objects.all()]
        sys_list = [{'id': 2, 'name': '蓝鲸'}]  # 临时
        admin_list = [{'id': 1, 'name': 'admin'}]  # 临时
        return render_json({'result': True, 'data': {
            "ip_pools": ip_pools,
            "sys_list": sys_list,
            "admin_list": admin_list
        }})
    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "data": [u"系统异常，请联系管理员"]})


def get_all_ips(request):
    try:
        filter_obj = json.loads(request.body)
        filter_data = []
        if filter_obj['ip_pools']:
            if not filter_obj['status']:
                filter_data = IPs.objects.filter(
                    owner__icontains=filter_obj['admin'],
                    business__icontains=filter_obj['sys'],
                    ip_pool_id=int(filter_obj['ip_pools']),
                    start_ip__icontains=filter_obj['ip'],
                    work_order__icontains=filter_obj['work_order']
                )
            else:
                filter_data = IPs.objects.filter(
                    owner__icontains=filter_obj['admin'],
                    business__icontains=filter_obj['sys'],
                    ip_pool_id=int(filter_obj['ip_pools']),
                    start_ip__icontains=filter_obj['ip'],
                    work_order__icontains=filter_obj['work_order'],
                    is_used=int(filter_obj['status'])
                )
        else:
            if not filter_obj['status']:
                filter_data = IPs.objects.filter(
                    owner__icontains=filter_obj['admin'],
                    business__icontains=filter_obj['sys'],
                    start_ip__icontains=filter_obj['ip'],
                    work_order__icontains=filter_obj['work_order']
                )
            else:
                filter_data = IPs.objects.filter(
                    owner__icontains=filter_obj['admin'],
                    business__icontains=filter_obj['sys'],
                    start_ip__icontains=filter_obj['ip'],
                    work_order__icontains=filter_obj['work_order'],
                    is_used=int(filter_obj['status'])
                )
        return_data = [
            {
                'id': i.id,
                'ip': i.start_ip,
                'mask': i.mask,
                'gateway': i.gateway,
                'is_used': i.is_used,
                'business': i.business,
                'owner': i.owner,
                'work_order': i.work_order,
                'ip_pool_name': i.ip_pool.title
            } for i in filter_data
        ]
        ip_pools = [{'id': i.id, 'name': i.title + '(' + i.ip_net + ')'} for i in IPPools.objects.all()]
        sys_list = [{'id': 2, 'name': '蓝鲸'}]

        return render_json({'result': True, 'data': return_data, 'sys_list': sys_list, 'ip_pools': ip_pools})
    except Exception as e:
        logger.exception("error:{0}".format(e.message))


def allocate_ips(request):
    try:
        re_data = json.loads(request.body)
        success_list = []
        allocate_logs = []
        for re in re_data:
            pool_id = IPPools.objects.get(title=re['ip_pool']).id
            is_in = IPs.objects.filter(ip_pool_id=pool_id, business=re['business'], owner=re['owner'],
                                       work_order=re['work_order'])
            if is_in:
                insert_log(u"自动分配IP失败", request.user.username,
                           "{0}/{1}/{2}/{3} 已有分配IP".format(re['ip_pool'], re['business'],
                                                           re['owner'],
                                                           re['work_order']))
                allocate_logs.append("该数据已分配，请勿重复分配！")
                continue
            if not pool_id:
                insert_log(u"自动分配IP失败", request.user.username,
                           "{0} 资源池不存在".format(re['ip_pool']))
                allocate_logs.append("{0} 资源池不存在".format(re['ip_pool']))
                continue
            if not re['ip_pool'] or not re['business'] or not re['owner'] or not re['work_order']:
                allocate_logs.append(
                    "{0}/{1}/{2}/{3} => 分配 ip 失败,原因：导入表格信息填写不完整".format(re['ip_pool'], re['business'], re['owner'],
                                                                        re['work_order']))
                insert_log(u"自动分配IP失败", request.user.username, "缺少必填项")
                return render_json({
                    "result": False,
                    "message": '导入表格信息填写不完整，请补充！',
                    "data": {'success': len(success_list), 'fail': len(re_data) - len(success_list)},
                    "allocate_logs": allocate_logs
                })
            avail_ips = [
                {
                    'id': i.id,
                    'ip': i.start_ip
                } for i in IPs.objects.filter(is_used=0, is_excluded=0, ip_pool_id=pool_id)
            ]
            if not len(avail_ips):
                insert_log(u"自动分配IP失败", request.user.username, "{0} 资源池 已无可分配ip".format(re['ip_pool']))
                return render_json({"result": False, "message": '该资源池已无可分配ip',
                                    "data": {'success': len(success_list),
                                             'fail': len(re_data) - len(success_list)},
                                    "allocate_logs": allocate_logs})

            random_ip = avail_ips[random.randint(0, len(avail_ips))]

            IPs.objects.filter(id=random_ip['id']).update(
                business=re['business'],
                owner=re['owner'],
                when_modified=date_now(),
                is_used=1,
                work_order=re['work_order']
            )
            success_list.append(re)
            allocate_logs.append("{0}/{1}/{2}/{3} => 分配 ip : {4}".format(re['ip_pool'], re['business'], re['owner'],
                                                                         re['work_order'], random_ip['ip']))
            insert_log(u"自动分配成功", request.user.username,
                       "{0}/{1}/{2}/{3} => 分配 ip : {4}".format(re['ip_pool'], re['business'], re['owner'],
                                                               re['work_order'], random_ip['ip']))
        return render_json({
            "result": True,
            "message": '分配完毕！',
            "data": {
                'success': len(success_list),
                'fail': len(re_data) - len(success_list)
            },
            "allocate_logs": allocate_logs
        })

    except Exception, e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "message": "系统异常，请联系管理员"})


@login_exempt
@csrf_exempt
def allocate_ip_api(request):
    try:
        allocate_data = json.loads(request.body)
        logger.error(allocate_data)
        ip_pool_name = allocate_data['ip_pool_name']
        pool_id = IPPools.objects.get(title=str(ip_pool_name)).id
        logger.error(pool_id)
        avail_ips = [
            {
                'id': i.id,
                'ip': i.start_ip
            } for i in IPs.objects.filter(is_used=0, is_excluded=0, ip_pool_id=int(pool_id))
        ]
        is_in = IPs.objects.filter(ip_pool_id=pool_id, business=allocate_data['sys'],
                                   owner=allocate_data['admin'],
                                   work_order=allocate_data['workOrder'])
        pool_title = IPPools.objects.get(id=pool_id).title
        if is_in:
            insert_log(u"手动分配IP失败", request.user.username,
                       "{0}/{1}/{2}/{3} 已有分配IP".format(pool_title, allocate_data['sys'],
                                                       allocate_data['admin'],
                                                       allocate_data['workOrder']))
            return render_json({"result": False, "message": '已分配，请勿重复分配！'})
        if not len(avail_ips):
            insert_log(u"手动分配IP失败", request.user.username, "{0} 资源池 已无可分配ip".format(pool_title))
            return render_json({"result": False, "message": '已无可分配ip'})

        random_ip = avail_ips[random.randint(0, (len(avail_ips))-1)]

        IPs.objects.filter(id=random_ip['id']).update(
            business=allocate_data['sys'],
            owner=allocate_data['admin'],
            when_modified=date_now(),
            is_used=1,
            work_order=allocate_data['workOrder']
        )
        return render_json({"result": True, "data": {'random_ip': random_ip['ip']}})

    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "data": [u"系统异常，请联系管理员"]})
@login_exempt
@csrf_exempt
def get_data(request):
    try:
        ip_pools = [{'id': i.id, 'name': i.title + '(' + i.ip_net + ')'} for i in IPPools.objects.all()]
        sys_list = [{'id': 2, 'name': '蓝鲸'}]  # 临时
        admin_list = [{'id': 1, 'name': 'admin'}]  # 临时
        return render_json({'result': True, 'data': {
            "ip_pools": ip_pools,
            "sys_list": sys_list,
            "admin_list": admin_list
        }})
    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "data": [u"系统异常，请联系管理员"]})