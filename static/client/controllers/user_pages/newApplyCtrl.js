controllers.controller("newApplyCtrl", function ($scope, ipPoolService, $filter, loading, errorModal, $modalInstance, applyService) {
    $scope.title = "新增申请";
    $scope.flag = false;
    var date_now = new Date();

    $scope.DateStart = date_now.setDate(date_now.getDate() + 30);
    $scope.ip_pool_list = [];
    ipPoolService.get_ip_pools({}, {}, function (res) {
        if (res.result)
            $scope.ip_pool_list = res.data;
    });
    $scope.applyObj = {
        ipType: "00",
        business: "",
        ips: "",
        apply_reason: "",
        ip_pool_id: ""
    };

    $scope.confirm = function () {
        var errors = validate();
        if (errors.length > 0) {
            errorModal.open(errors);
            return;
        }
        loading.open();
        applyService.create_apply({}, $scope.applyObj, function (res) {
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

    var validate = function () {
        var errors = [];
        if ($scope.applyObj.ip_pool_id == "") {
            errors.push("网段未选择！");
        }
        if ($scope.applyObj.business == "") {
            errors.push("业务系统不能为空！");
        }
        if ($scope.applyObj.apply_reason == "") {
            errors.push("申请理由不能为空！")
        }
        else if ($scope.applyObj.apply_reason.length > 100) {
            errors.push("申请理由超过100个字！")
        }
        var ipList = $scope.applyObj.ips.split(",");
        for (var i = 0; i < ipList.length; i++) {
            if (!CWApp.isIP(ipList[i])) {
                errors.push("IP格式不正确！");
                break;
            }
        }
        return errors;
    };

});