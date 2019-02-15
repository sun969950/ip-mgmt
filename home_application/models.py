# -*- coding: utf-8 -*-

from django.db import models
import datetime


class IPPools(models.Model):
    ip_start = models.CharField(max_length=50)
    ip_end = models.CharField(max_length=50)
    when_created = models.CharField(max_length=30)
    when_modified = models.CharField(max_length=30, default="")
    created_by = models.CharField(max_length=100)
    modified_by = models.CharField(max_length=100, default="")
    ip_net = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    all_count = models.IntegerField()
    range = models.CharField(max_length=1000)
    excute_range = models.CharField(max_length=1000)
    # used_count = models.IntegerField()
    assignable_count = models.IntegerField(null=True)
    threshold = models.CharField(max_length=100)
    use_rate = models.CharField(max_length=100)
    gateway = models.CharField(max_length=100)
    mask = models.CharField(max_length=100)

    def to_dic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

    def create_item(self, dict_item):
        self.ip_start = dict_item["ip_start"]
        self.ip_end = dict_item["ip_end"]
        self.created_by = dict_item["created_by"]
        self.title = dict_item["title"]
        self.ip_net = dict_item["ip_net"]
        self.all_count = dict_item["all_count"]
        self.assignable_count = dict_item["assignable_count"]
        self.when_created = str(datetime.datetime.now()).split(".")[0]
        self.range = dict_item["range"]
        self.excute_range = dict_item['excute_range']
        self.threshold = dict_item['threshold']
        self.use_rate = dict_item['use_rate']
        self.mask = dict_item['mask']
        self.gateway = dict_item['gateway']
        self.save()

    def modify_item(self, dict_item):
        self.ip_start = dict_item["ip_start"]
        self.ip_end = dict_item["ip_end"]
        self.modified_by = dict_item["modified_by"]
        self.title = dict_item["title"]
        self.ip_net = dict_item["ip_net"]
        self.all_count = dict_item["all_count"]
        self.assignable_count = dict_item["assignable_count"]
        self.when_modified = str(datetime.datetime.now()).split(".")[0]
        self.range = dict_item["range"]
        self.excute_range = dict_item['excute_range']
        self.threshold = dict_item['threshold']
        self.use_rate = dict_item['use_rate']
        self.mask = dict_item['mask']
        self.gateway = dict_item['gateway']
        self.save()


class Apply(models.Model):
    apply_num = models.CharField(max_length=20)
    when_created = models.CharField(max_length=20)
    when_expired = models.CharField(max_length=20)
    ip_list = models.TextField()

    # IP 类型：00表示IP，01表示网段
    ip_type = models.CharField(max_length=10)
    created_by = models.CharField(max_length=100)
    business = models.CharField(max_length=200)
    approved_by = models.CharField(max_length=100, default="", null=True)
    when_approved = models.CharField(max_length=20, default="", null=True)
    apply_reason = models.CharField(max_length=200)
    refuse_reason = models.CharField(max_length=200, default="", null=True)
    description = models.CharField(max_length=200, default="", null=True)
    # ip_pool = models.ForeignKey(IPPools, null=True, on_delete=models.SET_NULL)
    ip_pool = models.ForeignKey(IPPools)
    # 申请单状态：00表示已提交；01表示已通过；02表示被拒绝
    status = models.CharField(max_length=10, default="00")

    def to_dic(self):
        return_data = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields if f.name != "ip_pool"]])
        return_data["ip_pool"] = self.ip_pool.to_dic()
        return_data["ip_pool_name"] = self.ip_pool.title + "(" + self.ip_pool.ip_net + ")"
        return return_data


# class ResourceIPs(models.Model):
#     start_ip = models.CharField(max_length=20)
#     end_ip = models.CharField(max_length=20)
#     created_by = models.CharField(max_length=100)
#     modified_by = models.CharField(max_length=100)
#     when_created = models.CharField(max_length=100)
#     when_modified = models.CharField(max_length=20)
#     resource_type = models.CharField(max_length=20)
#
#     def to_dic(self):
#         return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class  IPs(models.Model):
    start_ip = models.CharField(max_length=20)
    end_ip = models.CharField(max_length=20)
    business = models.CharField(max_length=100, null=True, default="")
    # when_expired = models.CharField(max_length=20)
    owner = models.CharField(max_length=100)
    # is_expired = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100)
    modified_by = models.CharField(max_length=100)
    when_modified = models.CharField(max_length=100)
    when_created = models.CharField(max_length=100)
    # is_admin = models.BooleanField(default=False)
    # used_num = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)
    # is_assigned = models.BooleanField(default=False)
    is_excluded = models.BooleanField(default=False)
    # all_length = models.IntegerField(default=0)
    # ip_used_list = models.TextField(default="", null=True)
    description = models.CharField(max_length=200, default="", null=True)
    ip_pool = models.ForeignKey(IPPools)
    work_order = models.CharField(max_length=100)
    gateway = models.CharField(max_length=100)
    mask = models.CharField(max_length=100)

    def to_dic(self):
        return_data = dict(
            [(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields if f.name != "ip_used_list" and f.name != "ip_pool"]])
        return_data["ip_pool"] = self.ip_pool.to_dic()
        return_data["ip_pool_name"] = self.ip_pool.title + "(" + self.ip_pool.ip_net + ")"
        # if "[" not in self.ip_used_list:
        #     return_data["ip_used_list"] = [self.ip_used_list]
        # else:
        #     return_data["ip_used_list"] = eval(self.ip_used_list) if self.ip_used_list else []
        return return_data


class Logs(models.Model):
    operated_type = models.CharField(max_length=50)
    content = models.TextField()
    when_created = models.CharField(max_length=30)
    operator = models.CharField(max_length=50)

    def to_dic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class Mailboxes(models.Model):
    username = models.CharField(max_length=50)
    mailbox = models.CharField(max_length=100)
    when_created = models.CharField(max_length=30)

    def to_dic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class Settings(models.Model):
    key = models.CharField(max_length=50)
    value = models.TextField()
    description = models.CharField(max_length=100, null=True)

    def to_dic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])