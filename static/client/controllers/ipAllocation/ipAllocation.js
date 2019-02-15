/**
 * Created by cws on 2018/9/13.
 */
controllers.controller("ipAllocation", ["msgModal", "confirmModal", "$modal", "errorModal", "$scope", "ipService", "loading", "$timeout", function (msgModal, confirmModal, $modal, errorModal, $scope, ipService, loading, $timeout) {
    //tab切换
    $scope.index = 1;
    $scope.init_type = "model";
    $scope.is_init = false;
    $scope.changeTab = function (index) {
        $scope.index = index;
    };
    $scope.filterObj = {
        ipPool: '',
        sys: '',
        admin: '',
        workOrder: ''
    };
    $scope.poolList = [];
    $scope.sysList = [];
    $scope.adminList = [];

    $scope.allocate_result = '';
    $scope.status = '';


    $scope.search = function () {
        loading.open();
        ipService.get_relate_data({}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.poolList = res.data.ip_pools;
                $scope.sysList = res.data.sys_list;
                $scope.adminList = res.data.admin_list;
            }

        })
    };
    $scope.search()

    //分配
    $scope.allocate = function () {
        var error = $scope.isInvalidData();
        if (error.length > 0) {
            errorModal.open(error);
            return false;
        }
        ;
        loading.open();
        ipService.allocate_ip({}, $scope.filterObj, function (res) {
            loading.close();
            if (res.result) {
                $scope.status = "分配成功";
                $scope.allocate_result = res.data.random_ip;
                $scope.filterObj.ipPool = '';
                $scope.filterObj.admin = '';
                $scope.filterObj.sys = '';
                $scope.filterObj.workOrder = '';

            } else {
                $scope.status = "分配失败";
                $scope.allocate_result = res.message;
            }

        })
    };
    //验证
    $scope.isInvalidData = function () {
        var error = [];
        if (!$scope.filterObj.ipPool) {
            error.push("资源池不能为空！")
        }
        if (!$scope.filterObj.sys) {
            error.push("系统不能为空！")
        }
        if (!$scope.filterObj.admin) {
            error.push("管理员不能为空！")
        }
        if (!$scope.filterObj.workOrder) {
            error.push("工单号不能为空！")
        }
        return error;
    }

    //批量分配
    $scope.log_list = [];
    $scope.success_count = '';
    $scope.fail_count = '';
    $scope.uploadItem = function () {
        ajaxFileUpload("#uploadFile");
    };
    $scope.is_show = false;
    $scope.uploadCsv = function () {
        $scope.is_show  = true;
        var files = $("#uploadFile").get(0).files;
        if (!files.length) {
            msgModal.open("上传文件不能为空！");
            return
        }
        CWApp.uploadCsv("uploadFile", callBack);
    };

    var callBack = function () {
        var content = fr.result;
        content = content.replace(new RegExp("\"", "gm"), "");
        var temp_list = [];
        var content_list = content.substring(0, content.lastIndexOf("\n")).split("\n");
        var column_len = content_list[0].split(",").length;
        var one_errors = [];
        var up_cvs = function (data) {
            console.log(data);
            loading.open();
            ipService.allocate_ips({}, data, function (res) {
                loading.close()
                if (res.result) {
                    $scope.log_list = res.allocate_logs;
                    $scope.success_count = res.data.success;
                    $scope.fail_count = res.data.fail;
                    msgModal.open(res.message);
                    $scope.searchList();
                }
                else {
                    $scope.log_list = res.allocate_logs;
                    console.log($scope.log_list);
                    $scope.success_count = res.data.success;
                    $scope.fail_count = res.data.fail;
                    errorModal.open([res.message]);
                }
            })
        };
        for (var i = 1; i < content_list.length; i++) {
            var device_obj = {};
            var columns = content_list[i].replace("\r", "").split(",");
            console.log('column');
            console.log(columns);
            if (columns.length != column_len)
                continue;
            var device_obj = {
                ip_pool: columns[0],
                business: columns[1],
                owner: columns[2],
                work_order: columns[3]
            };
            temp_list.push(device_obj)
        }
        $scope.csvList = temp_list;
        up_cvs($scope.csvList)
    };

    //下载模板
    $scope.down_temp = function () {
        window.open('down_template');
    }

}]);
