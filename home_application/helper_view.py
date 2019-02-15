# -*- coding: utf-8 -*-

import os, sys, socket, threading, netaddr, multiprocessing, psutil, Queue
import django.utils.timezone as timezone
from home_application.models import Settings, IPs, Logs
from common.log import logger
import datetime
from home_application.models import IPPools
from django.db.models import Q


def date_now():
    date_now_str = str(timezone.now()).split(".")[0]
    return date_now_str


def ping_win(dest_addr, ping_timeout, count):
    try:
        ping_cmd = "ping %s -n %s -w %s" % (dest_addr, count, ping_timeout * 1000)
        res = os.system(ping_cmd)
        if res == 0:
            return dest_addr
    except:
        pass
    return None


def ping_lin(dest_addr, ping_timeout, count):
    try:
        ping_shell = "ping %s -c %s -w %s" % (dest_addr, count, ping_timeout)
        res = os.system(ping_shell)
        if res == 0:
            return dest_addr
    except:
        pass
    return None


def test_ping(dest_addr, ping_timeout, count):
    if sys.platform == "win32":
        return ping_win(dest_addr, ping_timeout, count)
    else:
        return ping_lin(dest_addr, ping_timeout, count)


def test_arping(dest_addr, arping_timeout, count, nic):
    try:
        arping_shell = "arping %s -c %s -w %s -I %s" % (dest_addr, count, arping_timeout, nic)
        res = os.system(arping_shell)
        if res == 0:
            return dest_addr
    except:
        pass
    return None


def get_nic():
    nic_name = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1] == '127.0.0.1':
                nic_name.append(k)
    return nic_name


def test_port(dst, port, port_timeout):
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_sock.settimeout(port_timeout)
    try:
        indicator = cli_sock.connect_ex((dst, port))
        if indicator == 0:
            return dst
        cli_sock.close()
    except:
        pass
    return None


def proxy(cls_instance, o):
    return cls_instance.NetScan(o)


class IPScan():
    """
    参数：
        ping_timeout    -- ping超时，默认3秒
        port_timeout    -- port超时，默认5秒
        ports      -- 默认扫描端口列表，数据类型为list
        count      -- ping扫描次数
    """

    def __init__(self, ping_timeout=2, port_timeout=2, count=2, ports=[22, 3389]):
        self.ping_timeout = ping_timeout
        self.port_timeout = port_timeout
        self.count = count
        self.ports = ports
        self.ip_list = []

    nics = get_nic()

    def ping_scan(self, ping_q, arp_q, port_q):
        while not ping_q.empty():
            dst_addr = ping_q.get()
            if dst_addr in self.ip_list:
                pass
            else:
                ip = test_ping(dst_addr, self.ping_timeout, self.count)
                if ip:
                    self.ip_list.append(ip)
                else:
                    for port in self.ports:
                        port_q.put((dst_addr, port))
                    for nic in self.nics:
                        arp_q.put((dst_addr, nic))
                    # if sys.platform == "win32":
                    #     for port in self.ports:
                    #         port_q.put((dst_addr, port))
                    # else:
                    #     for nic in self.nics:
                    #         arp_q.put((dst_addr, nic))
                ping_q.task_done()

    def arping_scan(self, arp_q):
        while not arp_q.empty():
            arg = arp_q.get()
            dst_addr = arg[0]
            nic_name = arg[1]
            if dst_addr in self.ip_list:
                pass
            else:
                ip = test_arping(dst_addr, self.ping_timeout, self.count, nic_name)
                if ip:
                    self.ip_list.append(ip)
                    # else:
                    #     for port in self.ports:
                    #         port_q.put((ip, port))
            arp_q.task_done()

    def port_scan(self, port_q):
        while not port_q.empty():
            arg = port_q.get()
            dst_addr = arg[0]
            port = arg[1]
            if dst_addr in self.ip_list:
                pass
            else:
                ip = test_port(dst_addr, port, self.port_timeout)
                if ip:
                    self.ip_list.append(ip)
            port_q.task_done()

    def NetScan(self, ipPool):
        ping_q = Queue.Queue()
        arp_q = Queue.Queue()
        port_q = Queue.Queue()
        for ip in ipPool:
            ping_q.put(ip)
        for num in xrange(20):
            tp = threading.Thread(target=self.ping_scan, args=(ping_q, arp_q, port_q))
            tp.start()
        ping_q.join()
        for num in xrange(20):
            tpo = threading.Thread(target=self.port_scan, args=(port_q,))
            tpo.start()
        port_q.join()
        if sys.platform != "win32":
            for num in xrange(20):
                ta = threading.Thread(target=self.arping_scan, args=(arp_q,))
                ta.start()
            arp_q.join()
        return list(set(self.ip_list))

    def NetScan1(self, ipPool):
        ping_q = Queue.Queue()
        arp_q = Queue.Queue()
        port_q = Queue.Queue()
        for ip in ipPool:
            ping_q.put(ip)
        for num in xrange(20):
            tp = threading.Thread(target=self.ping_scan, args=(ping_q, arp_q, port_q))
            tp.start()
        ping_q.join()
        for num in xrange(20):
            tpo = threading.Thread(target=self.port_scan, args=(port_q,))
            tpo.start()
        port_q.join()
        if sys.platform != "win32":
            for num in xrange(20):
                ta = threading.Thread(target=self.arping_scan, args=(arp_q,))
                ta.start()
            arp_q.join()
        return list(set(self.ip_list))


def list_changes(lists, num):
    for o in xrange(0, len(lists), num):
        yield lists[o:o + num]


def list_to_list(lists, num):
    list_temp = []
    for i in list_changes(lists, num):
        list_temp.append(i)
    return list_temp


def ippool_list(start_ip, end_ip):
    ip_list = [str(ip) for ip in netaddr.IPRange(start_ip, end_ip)]
    numP = multiprocessing.cpu_count() * 4
    num = (len(ip_list) + numP - 1) / numP
    ipPool_list = list_to_list(ip_list, num)
    return ipPool_list


def IPNetScan(start_ip, end_ip):
    port_str = Settings.objects.get(key="ports").value.split(",")
    po = [int(i) for i in port_str]
    ippoollist = ippool_list(start_ip, end_ip)
    s = IPScan(ports=po)
    ip_list = []
    if __name__ == "home_application.helper_view":
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        result = []
        for ippool in ippoollist:
            result.append(pool.apply_async(proxy, args=(s, ippool,)))
        pool.close()
        pool.join()
        for res in result:
            ip_list.extend(res.get())
    ip_list.sort(lambda x, y: cmp(''.join([i.rjust(3, '0') for i in x.split('.')]),
                                  ''.join([i.rjust(3, '0') for i in y.split('.')])))
    return ip_list


def IPNetScan1(start_ip, end_ip):
    port_str = Settings.objects.get(key="ports").value.split(",")
    po = [int(i) for i in port_str]
    ips_list = [str(ip) for ip in netaddr.IPRange(start_ip, end_ip)]
    s = IPScan(ports=po)
    ip_list = s.NetScan1(ips_list)
    ip_list.sort(lambda x, y: cmp(''.join([i.rjust(3, '0') for i in x.split('.')]),
                                  ''.join([i.rjust(3, '0') for i in y.split('.')])))
    return ip_list


# def IPNetScan2(start_ip, end_ip):
#     port_str = Settings.objects.get(key="ports").value.split(",")
#     po = [int(i) for i in port_str]
#     ips_list = [str(ip) for ip in netaddr.IPRange(start_ip, end_ip)]
#     s = IPScan(ports=po)
#     ip_list = s.NetScan2(ips_list)
#     ip_list.sort(lambda x, y: cmp(''.join([i.rjust(3, '0') for i in x.split('.')]),
#                                   ''.join([i.rjust(3, '0') for i in y.split('.')])))
#     return ip_list


def one_ip_scan(ip_addresses):
    port_str = Settings.objects.get(key="ports").value.split(",")
    po = [int(i) for i in port_str]
    s = IPScan(ports=po)
    ip_list = s.NetScan1(ip_addresses)
    return ip_list


def validate_ips(start_ip, end_ip):
    result = validate_networks(start_ip, end_ip)
    if not result["result"]:
        return result
    try:
        ip_allocation = []
        ip_all = IPs.objects.all()
        ip_apply_list = netaddr.IPRange(start_ip,end_ip)
        for u in ip_all:
            if u.start_ip in ip_apply_list or u.end_ip in ip_apply_list:
                return {"result": False, "data": [u"该网段已存在或者该网段有部分IP在其它网段内"]}
            ip_pools = netaddr.IPRange(u.start_ip, u.end_ip)
            ip_tem_list = [str(c) for c in ip_pools]
            ip_allocation += ip_tem_list
        if start_ip in ip_allocation or end_ip in ip_allocation:
            return {"result": False, "data": [u"该网段已存在或者该网段有部分IP在其它网段内"]}
        return {"result": True}
    except Exception, e:
        logger.exception(e)
        return {"result": False, "data": [u"系统出错，请联系管理员！"]}


def validate_networks(start_ip, end_ip):
    try:
        netaddr.IPRange(start_ip, end_ip)
        return {"result": True}
    except Exception, e:
        logger.exception(e)
        return {"result": False, "data": [u"网段开始IP比结束IP大！"]}


def validate_one_ips(ips,pool_id):
    try:
        # ip_allocation = []
        # ip_all = IPs.objects.all()
        # for u in ip_all:
        #     ip_pools = netaddr.IPRange(u.start_ip, u.end_ip)
        #     ip_tem_list = [str(c) for c in ip_pools]
        #     ip_allocation += ip_tem_list
        # for c in ips:
        #     if c in ip_allocation:
        #         return {"result": False, "data": [u"该IP已被分配"]}
        # return {"result": True}

        pool = IPPools.objects.get(id=pool_id)
        used_or_assigned_ip_list = pool.ips_set.filter(Q(is_used=True) | Q(is_assigned=True)).values_list("start_ip",
                                                                                                          flat=True)
        for ip in ips:
            if ip in used_or_assigned_ip_list:
                data = u"IP{0}已分配或正在使用".format(ip)
                return {"result": False, "data": [data]}
        return {"result": True}
    except Exception, e:
        logger.exception(e)
        return {"result": False, "data": [u"系统出错，请联系管理员"]}


def validate_ips_exclude_self(start_ip, end_ip, ip_id):
    result = validate_networks(start_ip, end_ip)
    if not result["result"]:
        return result
    try:
        ip_allocation = []
        ip_all = IPs.objects.exclude(id=ip_id)
        for u in ip_all:
            ip_pools = netaddr.IPRange(u.start_ip, u.end_ip)
            ip_tem_list = [str(c) for c in ip_pools]
            ip_allocation += ip_tem_list
        if start_ip in ip_allocation or end_ip in ip_allocation:
            return {"result": False, "data": [u"该网段已存在或者该网段有部分IP在其它网段内"]}
        return {"result": True}
    except Exception, e:
        logger.exception(e)
        return {"result": False, "data": [u"系统出错，请联系管理员！"]}


def insert_log(operated_type, operator, detail):
    date_now_str = str(datetime.datetime.now()).split('.')[0]
    Logs.objects.create(operated_type=operated_type, when_created=date_now_str, operator=operator, content=detail)
