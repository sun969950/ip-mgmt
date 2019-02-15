# -*- coding: utf-8 -*-

from common.mymako import render_json
from home_application.models import *
from home_application.celery_tasks import *
import datetime
import json


def add_mail(request):
    args = eval(request.body)
    username = args["username"]
    mailbox = args["mailbox"]
    try:
        now = str(datetime.datetime.now()).split('.')[0]
        mail = Mailboxes.objects.filter(mailbox=mailbox)
        if len(mail) == 1:
            return render_json({"result": False, "data": "此邮箱账号已存在"})
        mail_add = Mailboxes.objects.create(username=username, mailbox=mailbox, when_created=now)
        insert_log(u"邮箱管理", request.user.username, u"新增邮箱：%s" % mailbox)
        return render_json({'result': True, "data": mail_add.to_dic()})
    except Exception, e:
        err_msg = e.message if e.message else str(e)
        logger.exception(e)
        return render_json({"result": False, "data": err_msg})


def modify_mail(request):
    args = eval(request.body)
    mail_id = args["id"]
    username = args["username"]
    mailbox = args["mailbox"]
    try:
        # now = str(datetime.datetime.now()).split('.')[0]
        mail = Mailboxes.objects.filter(mailbox=mailbox).exclude(id=mail_id)
        if len(mail) == 1:
            return render_json({"result": False, "data": "此邮箱账号已存在"})
        mail_obj = Mailboxes.objects.get(id=mail_id)
        old_mailbox = mail_obj.mailbox
        mail_obj.username = username
        mail_obj.mailbox = mailbox
        mail_obj.save()
        insert_log(u"邮箱管理", request.user.username, u"修改邮箱：%s ==> %s" % (old_mailbox, mailbox))
        return render_json({'result': True, "data": mail_obj.to_dic()})
    except Exception, e:
        err_msg = e.message if e.message else str(e)
        logger.exception(err_msg)
        return render_json({"result": False, "data": err_msg})


def delete_mail(request):
    mail_id = request.GET["id"]
    try:
        mail_delete = Mailboxes.objects.get(id=mail_id)
        insert_log(u"邮箱管理", request.user.username, u"删除邮箱：%s" % mail_delete.mailbox)
        mail_delete.delete()
        return render_json({'result': True})
    except Exception, e:
        err_msg = e.message if e.message else str(e)
        logger.exception(err_msg)
        return render_json({"result": False, "data": err_msg})


def search_mail(request):
    args = eval(request.body)
    username = args["username"]
    mailbox = args["mailbox"]
    try:
        result = Mailboxes.objects.filter(username__icontains=username, mailbox__icontains=mailbox).order_by("-when_created")
        return_data = [i.to_dic() for i in result]
        return render_json({"result": True, "data": return_data})
    except Exception, e:
        err_msg = e.message if e.message else str(e)
        logger.exception(err_msg)
        return render_json({"result": False, "data": err_msg})


def search_log(request):
    filter_obj = json.loads(request.body)
    logs = Logs.objects.filter(
        when_created__range=(str(filter_obj["whenStart"]) + " 00:00:00", str(filter_obj["whenEnd"]) + " 23:59:59"),
        operated_type__icontains=filter_obj["operateType"],
        operator__icontains=filter_obj["operator"]).order_by("-id")
    return render_json({"is_success": True, "data": [i.to_dic() for i in logs]})
