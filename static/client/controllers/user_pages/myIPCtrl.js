controllers.controller("myIPCtrl", ["$scope", "ipService", "errorModal","loading", function ($scope, ipService, errorModal,loading) {
    $scope.ip_list = [];
    $scope.filterObj = {
        business: "",
        ip: "",
        created_by: ""
    };
    $scope.searchList = function () {
        loading.open();
        ipService.search_user_ips({}, $scope.filterObj, function (res) {
            loading.close();
            if (res.result) {
                $scope.ip_list = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
                // if (window.location.href.indexOf("#/segmentManagement") > -1)
                //     setTimeout($scope.searchList, 3000);
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
            {field: "start_ip", displayName: "IP", width: 150},
            {field: "business", displayName: "业务系统",width: 200},
            // {field: "owner", displayName: "管理员", width: 120},
            // {field: "description", displayName: "描述"},
            {field: "ip_pool_name", displayName: "所属资源池"},
            {field: "is_used", displayName: "是否已使用", width: 90},
            {field: "when_created", displayName: "创建时间", width: 200},
        ]
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