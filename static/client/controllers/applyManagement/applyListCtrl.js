controllers.controller('applyListCtrl', ["$scope", "$modal", "applyService", "confirmModal", "errorModal", "loading", function ($scope, $modal, applyService, confirmModal, errorModal, loading) {
    $scope.applyList = [];

    $scope.filterObj = {
        business: "",
        ip: "",
        created_by: ""
    };

    $scope.searchList = function () {
        loading.open();
        applyService.search_admin_apply({}, $scope.filterObj, function (res) {
            loading.close();
            if (res.result) {
                $scope.applyList = res.data;
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
        $scope.setPagingData($scope.applyList ? $scope.applyList : [], pageSize, page);
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
            {field: "apply_num", displayName: "申请单号", width: 110},
            {field: "business", displayName: "业务系统", width: 150},
            {field: "ip_list", displayName: "IP地址"},
            {field: "created_by", displayName: "申请人", width: 150},
            {field: "apply_reason", displayName: "申请理由", width: 150},
            {
                displayName: "操作", width: 160,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top:5px;">' +
                '<span class="label label-primary label-sm label-btn" ng-click="approveApply(row.entity)">审批</span>' +
                '<span style="margin-left: 5px;" class="label label-danger label-sm label-btn" ng-click="refuseApply(row.entity)">拒绝</span>' +
                '<span style="margin-left: 5px;" class="label label-info label-sm label-btn" ng-click="openDetail(row.entity)">详情</span>' +
                '</div>'
            }
        ]
    };

    $scope.approveApply = function (rowEntity) {
        confirmModal.open({
            text: "请确认是否要审批此申请单",
            confirmClick: function () {
                loading.open();
                applyService.approve_apply({}, rowEntity, function (res) {
                    loading.close();
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

    $scope.refuseApply = function (rowEntity) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/applyManagement/approveApply.html',
            windowClass: 'applyDialog',
            controller: 'approveApplyCtrl',
            backdrop: 'static',
            resolve: {
                item: function () {
                    return rowEntity;
                }
            }
        });
        modalInstance.result.then(function () {
            $scope.searchList();
        });
    };

    $scope.openDetail = function (rowEntity) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/user_pages/newApply.html',
            windowClass: 'applyDialog',
            controller: 'checkApplyCtrl',
            backdrop: 'static',
            resolve: {
                item: function () {
                    return rowEntity;
                }
            }
        });
    }
}]);