controllers.controller("modifyIPsCtrl", ["$scope", "$filter", "item", "ipPoolService", "loading", "errorModal", "$modalInstance", "ipService", "sysService", function ($scope, $filter, item, ipPoolService, loading, errorModal, $modalInstance, ipService, sysService) {
    $scope.title = "修改网段";

    $scope.ipObj = item;
    $scope.ipObj.ip_pool_id = item.ip_pool.id;
    $scope.userList = [];
    $scope.ip_pool_list = [];
    ipPoolService.get_ip_pools({}, {}, function (res) {
        if (res.result)
            $scope.ip_pool_list = res.data;
    });
    $scope.confirm = function () {
        var errors = validate();
        if (errors.length > 0) {
            errorModal.open(errors);
            return;
        }
        loading.open();
        for (var i in $scope.userList) {
            if ($scope.userList[i].id == $scope.ipObj.owner) {
                $scope.ipObj.owner_name = $scope.userList[i].text;
            }
        }
        ipService.modify_ips({}, $scope.ipObj, function (res) {
            loading.close();
            if (res.result) {
                $modalInstance.close();
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.init = function () {
        sysService.get_all_user({}, {}, function (res) {
            if (res.result) {
                $scope.userList = res.data;
                for (var i in res.data) {
                    if (res.data[i].text == $scope.ipObj.owner) {
                        $scope.ipObj.owner = res.data[i].id;
                        break;
                    }
                }
            }
            else
                errorModal.open(res.data);
        })
    };
    $scope.init();

    $scope.userOption = {
        data: "userList",
        modelData: "ipObj.owner"
    };
    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };

    var validate = function () {
        var errors = [];
        var oneError = CWApp.ValidateDate($filter, $scope.ipObj.when_expired);
        if (oneError != "") {
            errors.push(oneError);
        }
        if ($scope.ipObj.ip_pool_id == "") {
            errors.push("网段未选择！");
        }
        if (!CWApp.isIP($scope.ipObj.start_ip)) {
            errors.push("起始IP格式不正确！");
        }
        if (!CWApp.isIP($scope.ipObj.end_ip)) {
            errors.push("结束IP格式不正确！");
        }
        return errors;
    };
}]);