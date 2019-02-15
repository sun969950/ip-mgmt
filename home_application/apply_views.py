# -*- coding=utf-8 -*-
from common.mymako import render_json
from home_application.models import *
from home_application.celery_tasks import *
from home_application.helper_view import insert_log
import json
from conf.default import BK_PAAS_HOST, SITE_URL, APP_ID

from IPy import IP


def get_apply_ip_exist(ip_pool_list, ip_obj):
    if ip_obj["start_ip"] not in ip_pool_list:
        return False
    if ip_obj["end_ip"] not in ip_pool_list:
        return False
    return True


def create_apply(request):
    try:
        apply_obj = json.loads(request.body)
        ip_pool_list = IP(IPPools.objects.get(id=apply_obj["ip_pool_id"]).ip_net)
        if apply_obj["ipType"] == "00":
            ips = apply_obj["ips"].strip(",").split(",")
            # v_result = validate_one_ips(apply_obj["ips"])
            # if apply_obj["ips"] not in ip_pool_list:
            #     return render_json({"result": False, "data": [u"IP超出网段范围"]})
            # ip_list = apply_obj["ips"]

            for ip in ips:
                if ip not in ip_pool_list:
                    return render_json({"result": False, "data": [u"IP超出网段范围"]})
            ex_result = check_exclude_ip(ips, apply_obj["ip_pool_id"])
            v_result = validate_one_ips(ips, apply_obj["ip_pool_id"])
            ip_list = apply_obj["ips"]
        # else:
        #     if not get_apply_ip_exist(ip_pool_list, apply_obj):
        #         return render_json({"result": False, "data": [u"IP超出网段范围"]})
        #     v_result = validate_ips(apply_obj["start_ip"], apply_obj["end_ip"])
        #     ip_list = apply_obj["start_ip"] + "," + apply_obj["end_ip"]
        if not ex_result["result"]:
            return render_json(ex_result)
        if not v_result["result"]:
            return render_json(v_result)
        date_now_str = date_now()
        apply_num = date_now_str.split(" ")[0].replace("-", "")
        applies = Apply.objects.filter(apply_num__contains=apply_num).order_by("-apply_num")
        if applies.count():
            apply_num = str(int(applies[0].apply_num) + 1)
        else:
            apply_num += "0001"
        Apply.objects.create(
            apply_num=apply_num,
            when_created=date_now_str,
            ip_list=ip_list,
            ip_type=apply_obj["ipType"],
            created_by=request.user.username,
            business=apply_obj["business"],
            apply_reason=apply_obj["apply_reason"],
            ip_pool_id=apply_obj["ip_pool_id"]
        )
        # 发送邮件
        mails = Mailboxes.objects.all().values('mailbox')
        to = []
        for i in mails:
            if i['mailbox'] not in to:
                to.append(i['mailbox'])
        subject = '新增ip申请'
        content = u'收到新增IP的申请单，请到{0}#applyList 查看审批' \
            .format(BK_PAAS_HOST + SITE_URL)
        # send_mail(to, subject, content)
        receivers = ",".join(to)
        new_send_email.delay(receivers, subject, content)
        insert_log(u"申请单管理", request.user.username, u"新增申请单，申请单号：%s" % apply_num)
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def search_user_apply(request):
    try:
        filter_obj = eval(request.body)
        username = request.user.username
        apply_list = Apply.objects.filter(business__icontains=filter_obj["business"], created_by=username)
        return_data = []
        for a in apply_list:
            if a.ip_type == "01":
                ips = a.ip_list.split(",")
                ip_pool = netaddr.IPRange(ips[0], ips[1])
                ip_pool_str = str([str(u) for u in ip_pool])
                if filter_obj["ip"] in ip_pool_str:
                    apply_obj = a.to_dic()
                    apply_obj["status_name"] = u"待审批" if a.status == "00" else "已通过" if a.status == "01" else "被拒绝"
                    apply_obj["ip_list"] = apply_obj["ip_list"].replace(",", "~")
                    return_data.append(apply_obj)
            elif filter_obj["ip"] in a.ip_list:
                apply_obj = a.to_dic()
                apply_obj["status_name"] = u"待审批" if a.status == "00" else "已通过" if a.status == "01" else "被拒绝"
                return_data.append(apply_obj)
        return render_json({"result": True, "data": return_data})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def search_admin_apply(request):
    try:
        filter_obj = eval(request.body)
        apply_list = Apply.objects.filter(
            business__icontains=filter_obj["business"], status="00",
            created_by__icontains=filter_obj["created_by"]
        )
        return_data = []
        for c in apply_list:
            if c.ip_type == "01":
                ips = c.ip_list.split(",")
                ip_pool = netaddr.IPRange(ips[0], ips[1])
                ip_pool_str = str([str(u) for u in ip_pool])
                if filter_obj["ip"] in ip_pool_str:
                    one_data = c.to_dic()
                    one_data["ip_list"] = one_data["ip_list"].replace(",", "~")
                    return_data.append(one_data)
            elif filter_obj["ip"] in c.ip_list:
                return_data.append(c.to_dic())
        return render_json({"result": True, "data": return_data})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def search_complete_apply(request):
    try:
        filter_obj = eval(request.body)
        apply_list = Apply.objects.filter(
            business__icontains=filter_obj["business"],
            created_by__icontains=filter_obj["created_by"],
            status__icontains=filter_obj["status"]
        ).exclude(status="00")
        return_data = []
        for c in apply_list:
            if c.ip_type == "01":
                ips = c.ip_list.split(",")
                ip_pool = netaddr.IPRange(ips[0], ips[1])
                ip_pool_str = str([str(u) for u in ip_pool])
                if filter_obj["ip"] in ip_pool_str:
                    apply_obj = c.to_dic()
                    apply_obj["status_name"] = u"已通过" if c.status == "01" else u"被拒绝"
                    apply_obj["ip_list"] = apply_obj["ip_list"].replace(",", "~")
                    return_data.append(apply_obj)
            elif filter_obj["ip"] in c.ip_list:
                apply_obj = c.to_dic()
                apply_obj["status_name"] = u"已通过" if c.status == "01" else u"被拒绝"
                return_data.append(apply_obj)
        return render_json({"result": True, "data": return_data})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def approve_apply(request):
    try:
        apply_id = eval(request.body)["id"]
        date_now_str = date_now()
        apply_obj = Apply.objects.get(id=apply_id)
        apply_obj.when_approved = date_now_str
        apply_obj.approved_by = request.user.username
        apply_obj.save()
        result = update_ips(apply_obj)
        if result["result"]:
            apply_obj.status = "01"
            apply_obj.save()
        else:
            return render_json(result)
        insert_log(u"申请单管理", request.user.username, u"审核申请单，申请单号：%s" % apply_obj.apply_num)
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def refuse_apply(request):
    try:
        apply_obj = eval(request.body)
        date_now_str = date_now()
        Apply.objects.filter(id=apply_obj["id"]).update(
            status="02",
            refuse_reason=apply_obj["refuse_reason"],
            when_approved=date_now_str,
            approved_by=request.user.username
        )
        insert_log(u"申请单管理", request.user.username, u"拒绝申请单，申请单号：%s" % apply_obj["apply_num"])
        return render_json({"result": True})
    except Exception, e:
        logger.exception(e)
        return render_json({"result": False, "data": [u"系统出错，请联系管理员！"]})


def update_ips(apply_obj):
    try:
        ips = apply_obj.ip_list.strip(",").split(",")
        if apply_obj.ip_type == "00":
            v_result = validate_one_ips(apply_obj.ip_list, apply_obj.ip_pool.id)
            if not v_result["result"]:
                return v_result
            for c in ips:
                IPs.objects.filter(start_ip=c).update(
                    # start_ip=c,
                    # end_ip=c,
                    business=apply_obj.business,
                    owner=apply_obj.created_by,
                    # created_by=apply_obj.approved_by,
                    modified_by=apply_obj.approved_by,
                    when_modified=apply_obj.when_approved,
                    # is_assigned=True
                    # when_created=apply_obj.when_approved,
                    # all_length=1,
                    # ip_pool_id=apply_obj.ip_pool.id
                )
            # used_count = IPPools.objects.get(id=apply_obj.ip_pool.id).used_count + len(ips)
            # IPPools.objects.filter(id=apply_obj.ip_pool.id).update(used_count=used_count)
            # get_one_ip_usage.delay(ips)

        # else:
        #     v_result = validate_ips(ips[0], ips[1])
        #     if not v_result["result"]:
        #         return v_result
        #     all_length = len(netaddr.IPRange(ips[0], ips[1]))
        #
        #     ip_obj = IPs.objects.create(
        #         start_ip=ips[0],
        #         end_ip=ips[1],
        #         business=apply_obj.business,
        #         when_expired=apply_obj.when_expired,
        #         owner=apply_obj.created_by,
        #         created_by=apply_obj.approved_by,
        #         modified_by=apply_obj.approved_by,
        #         when_modified=apply_obj.when_approved,
        #         when_created=apply_obj.when_approved,
        #         all_length=all_length,
        #         description=apply_obj.description,
        #         ip_pool_id=apply_obj.ip_pool.id
        #     )
        #     used_count = IPPools.objects.get(id=apply_obj.ip_pool.id).used_count + all_length
        #     IPPools.objects.filter(id=apply_obj.ip_pool.id).update(used_count=used_count)
        #     get_ips_usage.delay(ip_obj)
        return {"result": True}
    except Exception, e:
        logger.exception(e)
        return {"result": False, "data": [u"系统出错，请联系管理员"]}


def check_exclude_ip(ips, pool_id):
    try:
        pool = IPPools.objects.get(id=pool_id)
        exclude_ip_list = list(pool.ips_set.filter(is_excluded=True).values_list("start_ip", flat=True))
        for ip in ips:
            if ip in exclude_ip_list:
                data=u"IP{0}被排除使用".format(ip)
                return {"result": False, "data": [data]}
        return {"result": True}
    except Exception, e:
        logger.exception(e)
        return {"result": False, "data": [u"系统出错，请联系管理员"]}