controllers.controller('mailAddCtrl', ["$scope", "sysService", "errorModal", "$modalInstance", "loading", function ($scope, sysService, errorModal, $modalInstance, loading) {
    $scope.title = "添加管理员邮箱";
    $scope.args = {
        username: current_user,
        mailbox: ""
    };
    $scope.confirm = function () {
        if(!CWApp.isMail($scope.args.mailbox)){
            errorModal.open(["邮箱格式有误"]);
            return;
        }
        loading.open();
        sysService.add_mail({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $modalInstance.close(res.data);
            }
            else {
                errorModal.open(res.data.split(";"));
            }
        })
    };
    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };
}]);