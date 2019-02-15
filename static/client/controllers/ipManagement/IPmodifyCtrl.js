controllers.controller("IPmodifyCtrl",["$scope","errorModal","$modal","loading","confirmModal","ipService","itemObj","$modalInstance", function ($scope, errorModal, $modal, loading, confirmModal, ipService,itemObj,$modalInstance) {
    $scope.title = "编辑IP";
    $scope.args = itemObj;
    $scope.confirm = function () {
        loading.open();
        ipService.modify_ip({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $modalInstance.close();
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };
}]);



