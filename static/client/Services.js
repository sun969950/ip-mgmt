services = angular.module('webApiService', ['ngResource', 'utilServices']);

//生产代码
var POST = "POST";
var GET = "GET";

//测试代码
//var sourceRoute = "./Client/MockData";
//var fileType = ".html";
//var POST = "GET";
//var GET = "GET";
services.factory('ipService', ['$resource', function ($resource) {
    return $resource(site_url + ':actionName/', {},
        {
            search_user_ips: {method: POST, params: {actionName: 'search_user_ips'}, isArray: false},
            search_used_ips: {method: POST, params: {actionName: 'search_used_ips'}, isArray: false},
            search_ip_assigned_not_used: {method: POST, params: {actionName: 'search_ip_assigned_not_used'}, isArray: false},
            create_ips: {method: POST, params: {actionName: 'create_ips'}, isArray: false},
            modify_ips: {method: POST, params: {actionName: 'modify_ips'}, isArray: false},
            delete_ips: {method: POST, params: {actionName: 'delete_ips'}, isArray: false},
            detect_ips: {method: POST, params: {actionName: 'detect_ips'}, isArray: false},
            allocation_search: {method: POST, params: {actionName: 'allocation_search'}, isArray: false},
            get_used_ips: {method: POST, params: {actionName: 'get_used_ips'}, isArray: false},
            search_exclude_ips: {method: POST, params: {actionName: 'search_exclude_ips'}, isArray: false},
            modify_ip: {method: POST, params: {actionName: 'modify_ip'}, isArray: false},
            delete_ip_exclude: {method: POST, params: {actionName: 'delete_ip_exclude'}, isArray: false},
            search_usable_ips: {method: POST, params: {actionName: 'search_usable_ips'}, isArray: false},
            sync_cmdb: {method: POST, params: {actionName: 'sync_cmdb'}, isArray: false},
            allocate_ip:{method: POST, params: {actionName: 'allocate_ip'}, isArray: false},
            get_relate_data:{method: POST, params: {actionName: 'get_relate_data'}, isArray: false},
            recycle_ip:{method: POST, params: {actionName: 'recycle_ip'}, isArray: false},
            get_all_ips:{method: POST, params: {actionName: 'get_all_ips'}, isArray: false},
            upload_usedIps:{method: POST, params: {actionName: 'upload_usedIps'}, isArray: false},
            allocate_ips:{method: POST, params: {actionName: 'allocate_ips'}, isArray: false},
        });
    }])
    .factory('applyService', ['$resource', function ($resource) {
        return $resource(site_url + ':actionName/', {},
            {
                search_user_apply: {method: POST, params: {actionName: 'search_user_apply'}, isArray: false},
                create_apply: {method: POST, params: {actionName: 'create_apply'}, isArray: false},
                search_admin_apply: {method: POST, params: {actionName: 'search_admin_apply'}, isArray: false},
                search_complete_apply: {method: POST, params: {actionName: 'search_complete_apply'}, isArray: false},
                approve_apply: {method: POST, params: {actionName: 'approve_apply'}, isArray: false},
                refuse_apply: {method: POST, params: {actionName: 'refuse_apply'}, isArray: false},
            });
    }])
    .factory('sysService', ['$resource', function ($resource) {
        return $resource(site_url + ':actionName/', {},
            {
                search_log: {method: POST, params: {actionName: 'search_log'}, isArray: false},
                add_mail: {method: POST, params: {actionName: 'add_mail'}, isArray: false},
                modify_mail: {method: POST, params: {actionName: 'modify_mail'}, isArray: false},
                delete_mail: {method: POST, params: {actionName: 'delete_mail'}, isArray: false},
                search_mail: {method: POST, params: {actionName: 'search_mail'}, isArray: false},
                get_all_user: {method: POST, params: {actionName: 'get_all_user'}, isArray: false}

            });
    }])
    .factory('siteService', ['$resource', function ($resource) {
        return $resource(site_url + ':actionName/', {},
            {
                get_count_obj: {method: POST, params: {actionName: 'get_count_obj'}, isArray: false},
            });
    }])
  .factory('ipPoolService', ['$resource', function ($resource) {
        return $resource(site_url + ':actionName/', {},
            {
                get_ip_pools: {method: POST, params: {actionName: 'get_ip_pools'}, isArray: false},
                create_ip_pool: {method: POST, params: {actionName: 'create_ip_pool'}, isArray: false},
                modify_ip_pool: {method: POST, params: {actionName: 'modify_ip_pool'}, isArray: false},
                delete_ip_pool: {method: POST, params: {actionName: 'delete_ip_pool'}, isArray: false},
                search_ip_pools: {method: POST, params: {actionName: 'search_ip_pools'}, isArray: false},
                upload_ippools:{method: POST, params: {actionName: 'upload_ippools'}, isArray: false},
            });
    }])
  .factory('uploadService', ['$resource', function ($resource) {
        return $resource(site_url + ':actionName/', {},
            {
                down_exclude_ips: {method: POST, params: {actionName: 'down_exclude_ips'}, isArray: false},

            });
    }])
;//这是结束符，请勿删除