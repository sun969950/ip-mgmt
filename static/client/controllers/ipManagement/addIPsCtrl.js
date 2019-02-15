controllers.controller("addIPsCtrl", function ($scope, $filter, loading, errorModal, $modalInstance, ipService, sysService, ipPoolService) {
    $scope.title = "新增网段";
    var date_now = new Date();
    $scope.userList = [];
    $scope.DateStart = date_now.setDate(date_now.getDate() + 30);

    $scope.ip_pool_list = [];
    ipPoolService.get_ip_pools({}, {}, function (res) {
        if (res.result)
            $scope.ip_pool_list = res.data;
    });

    $scope.ipObj = {
        business: "",
        start_ip: "",
        end_ip: "",
        when_expired: $filter('date')($scope.DateStart, 'yyyy-MM-dd'),
        description: "",
        owner: user_id,
        ip_pool_id:""
    };


    $scope.init = function () {
        sysService.get_all_user({}, {}, function (res) {
            if (res.result)
                $scope.userList = res.data;

            else
                errorModal.open(res.data);
        })
    };
    $scope.init();

    $scope.userOption = {
        data: "userList",
        modelData: "ipObj.owner"
    };

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
        ipService.create_ips({}, $scope.ipObj, function (res) {
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
        var oneError = CWApp.ValidateDate($filter, $scope.ipObj.when_expired);
        if (oneError != "") {
            errors.push(oneError);
        }
        if($scope.ipObj.ip_pool_id==""){
            errors.push("网段未选择！");
        }
        if ($scope.ipObj.owner == "") {
            errors.push("管理员未指定！");
        }
        if ($scope.ipObj.start_ip == "") {
            errors.push("起始IP不能为空！");
        }
        if (!CWApp.isIP($scope.ipObj.start_ip)) {
            errors.push("起始IP格式不正确！");
        }
        if ($scope.ipObj.end_ip == "") {
            errors.push("结束IP不能为空！");
        }
        if (!CWApp.isIP($scope.ipObj.end_ip)) {
            errors.push("结束IP格式不正确！");
        }

        return errors;
    };
});