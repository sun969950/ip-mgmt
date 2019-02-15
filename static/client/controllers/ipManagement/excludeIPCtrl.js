controllers.controller("excludeIPCtrl",["$scope","errorModal","$modal","loading","confirmModal","ipService","uploadService", function ($scope, errorModal, $modal, loading, confirmModal, ipService,uploadService) {
    $scope.exclude_ip_list = [];
    $scope.args = {
        ip: "",
        ip_pools:""
    };
    $scope.pool_list = [];
    $scope.searchList = function () {
        loading.open();
        ipService.search_exclude_ips({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $scope.exclude_ip_list = res.data;
                $scope.pool_list = res.pool_list;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.searchList();

    $scope.modify_ip = function (row) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/ipManagement/IPmodify.html',
            windowClass: 'dialog_custom',
            controller: 'IPmodifyCtrl',
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

    $scope.delete_ip = function (row) {
        confirmModal.open({
            text: "确认不再排除该IP吗？",
            confirmClick: function () {
                ipService.delete_ip_exclude({}, row.entity, function (res) {
                    if (res.result) {
                        $scope.searchList();
                    }
                    else {
                        errorModal.open(res.data);
                    }
                })
            }
        })
    };

    $scope.Pagingdata = [];
    $scope.totalSerItems = 0;
    $scope.pagingOptions = {
        pageSizes: [5, 10, 25, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.exclude_ip_list ? $scope.exclude_ip_list : [], pageSize, page);
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
            {field: "start_ip", displayName: "排除IP", width: 120},
            {field: "ip_pool_name", displayName: "所属资源池",width: 200},
            // {field: "is_used", displayName: "是否已使用", width: 90},
            {field: "when_created", displayName: "创建时间", width: 200},
            {field: "description", displayName: "备注"},
            {
                displayName: '操作', width: 180,
                cellTemplate: '<div style="height: 34px;line-height: 34px;text-align: center;width: 100%;">' +
                '<span ng-click="modify_ip(row)" class="label label-info" style="padding: 5px;margin-left: 5px;cursor:pointer;">添加备注</span>' +
                '<span ng-click="delete_ip(row)" class="label label-danger" style="padding: 5px;margin-left: 5px;cursor:pointer;">删除</span>' +
                '</div>'
            }

        ]
    };




    $scope.down_cvs = function(){
        var url = "down_exclude_ips?"+"ip="+$scope.args.ip+'&ip_pools='+$scope.args.ip_pools;
        window.open(url);
    }
}]);



