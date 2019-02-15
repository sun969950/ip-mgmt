# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from esb.new_client import get_new_esb_client
from home_application.helper_view import *
from common.log import logger
from esb.client import *
import requests
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from blueking.component.shortcuts import *
from home_application.models import IPs
import netaddr

@task()
def send_mail(to, subject, mail_content, content_type="HTML"):
    if not to:
        return
    client = get_esb_client()

    kwargs = {
        "to": to,
        "subject": subject,
        "content": mail_content,
        "content_type": content_type,
    }
    result = client.call("common", "send_email", kwargs)
    if result["result"]:
        logger.error(u"邮件发送成功")
    else:
        logger.error(result["message"])

@task()
def new_send_email(receiver, title, content):
    try:
        logger.error(u"开始发送邮件")
        esb_client = get_new_esb_client()
        result = esb_client.call('cmsi','send_mail', receiver=receiver, title=title, content=content)
        if result["result"]:
            logger.error(u"邮件发送成功")
            return
        else:
            logger.error(u"邮件发送失败")
            logger.error(result["message"])
            return
    except Exception, e:
        logger.exception(e)


@task()
def get_one_ip_usage(ips):
    try:
        logger.info(u"开始扫描单个IP的使用情况")
        v_result = one_ip_scan(ips)
        for u in v_result:
            IPs.objects.filter(start_ip=u).update(used_num=1, ip_used_list=u)
        logger.info(u"结果写入成功")
        return True
    except Exception, e:
        logger.error(u"扫描IP使用情况出错；")
        logger.exception(e)


@task()
def get_ips_usage(ip_obj):
    try:
        logger.info(u"开始扫描网段的使用情况")
        v_result = IPNetScan1(ip_obj.start_ip, ip_obj.end_ip)
        ip_obj.used_num = len(v_result)
        ip_obj.ip_used_list = str(v_result)
        ip_obj.save()
        logger.info(u"结果写入成功")
        return True
    except Exception, e:
        logger.error(u"扫描IP使用情况出错；")
        logger.exception(e)


# @periodic_task(run_every=crontab(minute=0, hour='10,22', day_of_week="*"))
# def auto_update_ip():
#     all_ip = IPs.objects.filter(is_admin=True)
#     for i in all_ip:
#         get_ips_usage(i)
#     return True


# @periodic_task(run_every=crontab(minute="*/15"))
# def auto_update_ip_pool():
#     ip_pool_list = IPPools.objects.all()
#     for i in ip_pool_list:
#         update_ip_used(i)
#     return True

# @task()
# def update_ip_used(ip_pool):
#     ip_list = IPs.objects.filter(ip_pool_id=ip_pool.id)
#     used_count = 0
#     for i in ip_list:
#         start_ip = i.start_ip
#         end_ip = i.end_ip
#         used_count += len(netaddr.IPRange(start_ip, end_ip))
#     ip_pool.used_count = used_count
#     ip_pool.save()

@periodic_task(run_every=crontab(minute="*/10"))
def auto_update_ip_used():
    try:
        update_ip_used()
        return True
    except Exception, e:
        logger.exception(e)
        return False


def update_ip_used():
    cmdb_used_ips = set(get_servers())
    local_ips = set(IPs.objects.all().values_list("start_ip", flat=True))
    local_used_ips = set(IPs.objects.filter(is_used=True).values_list("start_ip", flat=True))
    cmdb_in_local_ips = cmdb_used_ips.intersection(local_ips)
    update_to_used_ips = cmdb_in_local_ips - local_used_ips
    update_to_unused_ips = local_used_ips - cmdb_in_local_ips
    for ip in update_to_used_ips:
        IPs.objects.filter(start_ip=ip).update(is_used=True)
        insert_log(u"IP管理", u'cmdb', u"更新IP状态为已使用：IP--%s" % (ip))
    for ip in update_to_unused_ips:
        IPs.objects.filter(start_ip=ip).update(is_used=False)
        insert_log(u"IP管理", u'cmdb', u"更新IP状态为未使用：IP--%s" % (ip))
    ip_pools = IPPools.objects.all()
    for ip_pool in ip_pools:
        ip_pool.assignable_count = ip_pool.ips_set.filter(is_used=False,is_excluded=False).count()
        ip_pool.save()


def get_servers():
    apps = get_app_by_user("admin")["data"]
    server_list = []
    for i in apps:
        server_result = get_host_list_by_business(i["id"], "admin")
        server_list.extend(server_result["data"])
    return [server["InnerIP"] for server in server_list]


def get_app_by_user(username):
    client = get_client_by_user(username)
    kwargs = {
        "app_code": APP_ID,
        "app_secret": APP_TOKEN,
        "username": username,
    }
    result = client.cc.get_app_by_user(kwargs)
    if result["result"]:
        app_list = [{"id": i["ApplicationID"], "text": i["ApplicationName"]} for i in result["data"] if
                    i["ApplicationName"] != u"资源池"]
        return {"result": True, "data": app_list}
    else:
        logger.error(result["message"])


def get_host_list_by_business(business_id, username):
    client = get_client_by_user(username)
    kwargs = {
        "app_code": APP_ID,
        "app_secret": APP_TOKEN,
        "username": username,
        "app_id": business_id
    }
    result = client.cc.get_app_host_list(kwargs)
    return result

