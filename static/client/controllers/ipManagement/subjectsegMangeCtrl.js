controllers.controller('subjectsegMangeCtrl', ["$scope", "ipService", "$modal", "loading", "errorModal", "confirmModal", function ($scope, ipService, $modal, loading, errorModal, confirmModal) {
    $scope.ip_list = [];
    $scope.filterObj = {
        business: "",
        ip: "",
        created_by: ""
    };
    $scope.searchList = function () {
        loading.open()
        ipService.search_ip_assigned_not_used({}, $scope.filterObj, function (res) {
            loading.close()
            if (res.result) {
                $scope.ip_list = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    $scope.searchList();
    $scope.Pagingdata = [];
    $scope.totalSerItems = 0;
    $scope.pagingOptions = {
        pageSizes: [5, 10, 25, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.ip_list ? $scope.ip_list : [], pageSize, page);
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
            {field: "start_ip", displayName: "IP", width: 120},
            {field: "business", displayName: "业务系统", width: 150},
            {field: "ip_pool_name", displayName: "所属资源池",width: 150},
            {field: "owner", displayName: "管理员", width: 120},
            // {field: "is_used", displayName: "是否已使用", width: 90},
            {field: "when_created", displayName: "创建时间", width: 150},
            {field: "description", displayName: "备注"},
            {
                displayName: "操作", width: 150,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top:5px;">' +
                '<span class="label label-info label-sm label-btn" ng-click="modifyItem(row)">编辑</span>&nbsp;' +
                '<span class="label label-danger label-sm label-btn" ng-click="deleteItem(row)">回收</span>' +
                '</div>'
            }
        ]
    };

    // $scope.addIPs = function () {
    //     var modalInstance = $modal.open({
    //         templateUrl: static_url + 'client/views/ipManagement/addIPs.html',
    //         windowClass: 'applyDialog',
    //         controller: 'addIPsCtrl',
    //         backdrop: 'static'
    //     });
    //     modalInstance.result.then(function () {
    //         $scope.searchList();
    //     });
    // };
    //
    $scope.modifyItem = function (row) {
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

    $scope.deleteItem = function (row) {
        confirmModal.open({
            text: "请确认是否回收该IP",
            confirmClick: function () {
                ipService.delete_ips({
                    id: row.entity.id
                }, {}, function (res) {
                    if (res.result) {
                        $scope.ip_list.splice(row.rowIndex, 1);
                        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
                    }
                    else {
                        errorModal.open(res.data);
                    }
                })
            }
        })
    };
    // $scope.isShowDetail = false;
    // $scope.selectItem = {};
    // $scope.detailItem = function (rowEntity) {
    //     $scope.selectItem = rowEntity;
    //     $scope.isShowDetail = true;
    //
    // };
    // $scope.returnBack = function () {
    //     $scope.isShowDetail = false;
    //
    // }
}]);