/**
 * Created by cws on 2018/9/18.
 */
controllers.controller('ipAll', ["$scope", "ipService", "$modal", "loading", "errorModal", "confirmModal","msgModal", function ($scope, ipService, $modal, loading, errorModal, confirmModal,msgModal) {
    $scope.ip_list = [];
    $scope.filterObj = {
        business: "",
        ip: "",
        ip_pools: "",
        admin: "",
        work_order: "",
        sys:'',
        status:''
    };
    $scope.pool_list = [];
    $scope.sys_list = [];
    $scope.status_list = [
        {'status':0,'name':"未使用"},
        {'status':1,'name':"已使用"},
    ]
    $scope.searchList = function () {
        loading.open();
        ipService.get_all_ips({}, $scope.filterObj, function (res) {
            loading.close();
            if (res.result) {
                $scope.ip_list = res.data;
                $scope.pool_list = res.ip_pools;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            } else {
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
            {field: "ip_pool_name", displayName: "资源池",width: 150},
            {field: "ip", displayName: "IP地址"},
            {field: "mask", displayName: "掩码"},
            {field: "gateway", displayName: "网关"},
            {
                field: "is_used",
                displayName: "使用状态",
                cellTemplate: '<div ng-if="row.entity.is_used" style="padding-left: 5px;">使用中</div>' +
                '<div ng-if="!row.entity.is_used" style="padding-left: 5px;">未使用</div>'
            },
            {field: "business", displayName: "业务系统"},
            {field: "owner", displayName: "管理员"},
            {field: "work_order", displayName: "工单号"}
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
    // $scope.deleteItem = function (row) {
    //     confirmModal.open({
    //         text: "请确认是否删除该网段",
    //         confirmClick: function () {
    //             ipService.delete_ips({
    //                 id: row.entity.id
    //             }, {}, function (res) {
    //                 if (res.result) {
    //                     $scope.ip_list.splice(row.rowIndex, 1);
    //                     $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    //                 }
    //                 else {
    //                     errorModal.open(res.data);
    //                 }
    //             })
    //         }
    //     })
    // };
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