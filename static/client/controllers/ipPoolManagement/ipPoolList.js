controllers.controller("ipPoolList", ["$scope", "msgModal", "errorModal", "$modal", "loading", "confirmModal", "ipPoolService", function ($scope, msgModal, errorModal, $modal, loading, confirmModal, ipPoolService) {
    $scope.pool_list = [];
    $scope.args = {
        title: "",
        ip_net:""
    };
    $scope.searchList = function () {
        loading.open();
        ipPoolService.search_ip_pools({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $scope.pool_list = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.searchList();


    $scope.addObj = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/ipPoolManagement/addIPPool.html',
            windowClass: 'dialog_custom',
            controller: 'addIPPool',
            backdrop: 'static'
        });
        modalInstance.result.then(function (res) {
            $scope.pool_list.push(res);
            $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            $scope.searchList();
        })
    };

    $scope.modify_pool = function (row) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/ipPoolManagement/addIPPool.html',
            windowClass: 'dialog_custom',
            controller: 'modifyIPPool',
            backdrop: 'static',
            resolve: {
                itemObj: function () {
                    return angular.copy(row.entity);
                }
            }
        });
        modalInstance.result.then(function () {
            $scope.searchList();
        })
    };

    $scope.delete_obj = function (row) {
        confirmModal.open({
            text: "确认删除该资源池吗？",
            confirmClick: function () {
                ipPoolService.delete_ip_pool({}, row.entity, function (res) {
                    if (res.result) {
                        $scope.pool_list.splice(row.rowIndex, 1);
                        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
                    }
                    else {
                        errorModal.open(res.data);
                    }
                })
            }
        })
    };
    //导入资源池
    $scope.uploadCsv = function () {
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
            ipPoolService.upload_ippools({}, data, function (res) {
                loading.close()
                if (res.result) {
                    msgModal.open('success', '上传成功！');
                    $scope.searchList();
                }
                else {
                    msgModalN.open(res.msg);
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
                ip_net: columns[0],
                title: columns[1] || '',
                range: columns[2]
            };
            temp_list.push(device_obj)
        }
        $scope.csvList = temp_list;
        up_cvs($scope.csvList)
    };

    $scope.Pagingdata = [];
    $scope.totalSerItems = 0;
    $scope.pagingOptions = {
        pageSizes: [5, 10, 25, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.pool_list ? $scope.pool_list : [], pageSize, page);
    };
    $scope.setPagingData = function (data, pageSize, page) {
        $scope.Pagingdata = data.slice((page - 1) * pageSize, page * pageSize);
        $scope.totalSerItems = data.length;
        if (!$scope.$$phase) {
            $scope.$apply();
        }
    };

    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    }, true);
    $scope.gridOption = {
        data: "Pagingdata",
        enablePaging: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: 'title', displayName: '名称'},
            {field: 'ip_net', displayName: '网段',width:100},
            {
                field: 'ip_range',
                displayName: '区间',
                width: 200,
                cellTemplate: '<span ng-if="row.entity.ip_range" ng-repeat="i in row.entity.range" style="height: 34px;line-height: 34px;" title="{{row.entity.ip_range}}">[{{i.ip_start}},{{i.ip_end}}],</span>'
            },
            {field: 'mask', displayName: '掩码',width:100},
            {field: 'gateway', displayName: '网关',width:100},
            {field: 'all_count', displayName: 'IP总数'},
            {field: 'assignable_count', displayName: 'IP可分配数量',width:100},
            {
                field: 'use_rate',
                displayName: '使用率',
                cellTemplate:'<span ng-if="row.entity.use_rate <= row.entity.threshold" style="height: 34px;line-height: 34px;">{{row.entity.use_rate}}%</span>' +
                '<span ng-if="row.entity.use_rate > row.entity.threshold" style="height: 34px;line-height: 34px;color: red;">{{row.entity.use_rate}}%</span>'
            },
            {
                field: 'threshold',
                displayName: '阈值',
                cellTemplate:'<span style="height: 34px;line-height: 34px;">{{row.entity.threshold}}%</span>'
            },
            {
                displayName: '操作', width: 180,
                cellTemplate: '<div style="height: 34px;line-height: 34px;text-align: center;width: 100%;">' +
                '<span ng-click="modify_pool(row)" class="label label-info" style="padding: 5px;margin-left: 5px;cursor:pointer;">编辑</span>' +
                '<span ng-click="delete_obj(row)" class="label label-danger" style="padding: 5px;;margin-left: 5px;cursor:pointer;">删除</span>' +
                '</div>'
            }

        ]
    };
}]);



