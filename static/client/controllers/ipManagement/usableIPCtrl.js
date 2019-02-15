controllers.controller("usableIPCtrl", ["$scope", "errorModal", "$modal", "loading", "confirmModal", "ipService", function ($scope, errorModal, $modal, loading, confirmModal, ipService) {
    $scope.usable_ip_list = [];
    $scope.filterObj = {
        ip: "",
        ip_pools: ""
    };
    $scope.pool_list = [];
    $scope.searchList = function () {
        loading.open();
        ipService.search_usable_ips({}, $scope.filterObj, function (res) {
            loading.close();
            if (res.result) {
                $scope.usable_ip_list = res.data;
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
    //
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

    $scope.sync_cmdb = function () {
        loading.open();
        ipService.sync_cmdb({}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.searchList();
            } else {
                errorModal.open(res.data)
            }
        })
    };
    //
    // $scope.delete_ip = function (row) {
    //     confirmModal.open({
    //         text: "确认不再排除该IP吗？",
    //         confirmClick: function () {
    //             ipService.delete_ip_exclude({}, row.entity, function (res) {
    //                 if (res.result) {
    //                     $scope.searchList();
    //                 }
    //                 else {
    //                     errorModal.open(res.data);
    //                 }
    //             })
    //         }
    //     })
    // };
    //
    $scope.Pagingdata = [];
    $scope.totalSerItems = 0;
    $scope.pagingOptions = {
        pageSizes: [5, 10, 25, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.usable_ip_list ? $scope.usable_ip_list : [], pageSize, page);
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
            {field: "ip_pool_name", displayName: "资源池"},
            {field: "start_ip", displayName: "IP"},
            {field: "mask", displayName: "掩码"},
            {field: "gateway", displayName: "网关"},
            {
                field: "is_used",
                displayName: "状态",
                cellTemplate:'<div ng-if="!row.entity.is_used" style="padding-left: 5px;">未使用</div>'
            }
            /*{
                displayName: '操作', width: 180,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                '<span ng-click="modify_ip(row)" class="label label-info" style="min-width:50px;margin-left: 5px;cursor:pointer;">添加备注</span>' +
                // '<span ng-click="delete_ip(row)" class="label label-danger" style="min-width:50px;margin-left: 5px;cursor:pointer;">删除</span>' +
                '</div>'
            }*/

        ]
    };

    $scope.down_cvs = function () {
        var url = "down_useable_ips?" + "ip=" + $scope.filterObj.ip + '&ip_pools=' + $scope.filterObj.ip_pools;
        window.open(url);
    };
}]);



