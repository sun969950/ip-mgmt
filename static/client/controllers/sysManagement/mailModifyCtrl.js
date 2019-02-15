controllers.controller('mailModifyCtrl', ["$scope", "errorModal", "objectItem", "sysService", "$modalInstance", "loading", function ($scope, errorModal, objectItem, sysService, $modalInstance, loading) {
    $scope.title = "修改邮箱";
    $scope.args = {
        id: objectItem.id,
        username: objectItem.username,
        mailbox: objectItem.mailbox,
    };
    $scope.confirm = function () {
        if (!CWApp.isMail($scope.args.mailbox)) {
            errorModal.open(["邮箱格式有误"]);
            return;
        }
        loading.open();
        sysService.modify_mail({}, $scope.args, function (res) {
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