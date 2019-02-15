controllers.controller('completedApplyCtrl', ["$scope", "applyService", "$modal", "errorModal", "loading", function ($scope, applyService, $modal, errorModal, loading) {

    $scope.applyList = [];

    $scope.filterObj = {
        business: "",
        ip: "",
        created_by: "",
        status: "0"
    };

    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.applyList ? $scope.applyList : [], pageSize, page);
    };
$scope.Pagingdata = [];
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
    $scope.searchList = function () {
        loading.open();
        applyService.search_complete_apply({}, $scope.filterObj, function (res) {
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

    $scope.gridOption = {
        data: "Pagingdata",
        enablePaging: true,
        showFooter: true,
        totalServerItems: 'totalSerItems',
        pagingOptions: $scope.pagingOptions,
        columnDefs: [
            {field: "apply_num", displayName: "申请单号", width: 110},
            {field: "business", displayName: "业务系统", width: 180},
            {field: "ip_list", displayName: "IP地址"},
            {field: "created_by", displayName: "申请人", width: 150},
            {field: "when_created", displayName: "申请时间", width: 150},
            {field: "status_name", displayName: "状态", width: 50},
            {
                displayName: "操作", width: 70,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top:5px;">' +
                '<span class="label label-info label-sm label-btn" ng-click="openDetail(row.entity)">详情</span>' +
                '</div>'
            }
        ]
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