# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    # 首页--your index
    (r'^$', 'home'),
    # (r'^user/$', 'user'),
    (r'^api/search_usable_ips/$', 'api_search_usable_ips'),
    (r'^api/lock_usable_ip/$', 'api_lock_usable_ip'),
    (r'^api/unlock_ip/$', 'api_unlock_ip'),
    (r'^get_count_obj$', 'get_count_obj'),
    # 申请单管理
    (r'^search_user_apply$', 'search_user_apply'),
    (r'^search_complete_apply$', 'search_complete_apply'),
    (r'^search_admin_apply$', 'search_admin_apply'),
    (r'^approve_apply$', 'approve_apply'),
    (r'^refuse_apply$', 'refuse_apply'),
    (r'^create_apply$', 'create_apply'),
    # IP管理
    (r'^search_user_ips$', 'search_user_ips'),
    (r'^search_used_ips$', 'search_used_ips'),
    (r'^search_ip_assigned_not_used$', 'search_ip_assigned_not_used'),
    (r'^create_ips$', 'create_ips'),
    (r'^modify_ips$', 'modify_ips'),
    (r'^allocation_search$', 'allocation_search'),
    (r'^detect_ips$', 'detect_ips'),
    (r'^delete_ips$', 'delete_ips'),
    (r'^get_all_user$', 'get_all_user'),
    (r'^search_exclude_ips$', 'search_exclude_ips'),
    (r'^modify_ip$', 'modify_ip'),
    (r'^recycle_ip$','recycle_ip'),
    (r'^delete_ip_exclude$', 'delete_ip_exclude'),
    (r'^search_usable_ips$', 'search_usable_ips'),
    (r'^sync_cmdb$', 'sync_cmdb'),
    (r'^allocate_ip$', 'allocate_ip'),
    (r'^allocate_ip_api$', 'allocate_ip_api'),
    (r'^get_relate_data$', 'get_relate_data'),
    (r'^get_data$', 'get_data'),
    (r'^get_all_ips$', 'get_all_ips'),
    (r'^upload_usedIps$', 'upload_usedIps'),
    (r'^allocate_ips$', 'allocate_ips'),
    # 系統管理
    (r'^add_mail$', 'add_mail'),
    (r'^modify_mail$', 'modify_mail'),
    (r'^delete_mail$', 'delete_mail'),
    (r'^search_mail$', 'search_mail'),
    (r'^search_log$', 'search_log'),
    # 资源池管理
    (r'^get_ip_pools$', 'get_ip_pools'),
    (r'^create_ip_pool$', 'create_ip_pool'),
    (r'^modify_ip_pool$', 'modify_ip_pool'),
    (r'^delete_ip_pool$', 'delete_ip_pool'),
    (r'^search_ip_pools$', 'search_ip_pools'),
    #导入cvs
    (r'^upload_ippools$','upload_ippools'),
    (r'^down_exclude_ips$','down_exclude_ips'),
    (r'^down_used_ips$','down_used_ips'),
    (r'^down_useable_ips$','down_useable_ips'),
    (r'^down_template$','down_template')
)
