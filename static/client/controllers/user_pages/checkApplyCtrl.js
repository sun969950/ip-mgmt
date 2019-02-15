controllers.controller("checkApplyCtrl", ["$scope", "$modalInstance", "item", function ($scope, $modalInstance, item) {
    $scope.title = "查看申请";
    $scope.flag = true;
    $scope.applyObj = item;
    $scope.applyObj.ipType = item.ip_type;
    $scope.applyObj.ips = item.ip_list;
    $scope.isShow = item.refuse_reason != "";

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };

}]);