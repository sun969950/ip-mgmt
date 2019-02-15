controllers.controller('addIPPool', ["$scope", "ipPoolService", "errorModal", "$modalInstance", "loading", function ($scope, ipPoolService, errorModal, $modalInstance, loading) {
    $scope.title = "添加IP资源池";
    $scope.args = {
        title: "",
        ip_net: "",
        threshold:null,
        mask:"",
        gateway:"",
        interval_list: [{
            index: 1,
            ip_start: "",
            ip_end: ""
        }],
        excute_range: [{
            index: 1,
            ip_start: "",
            ip_end: ""
        }]
    };
    $scope.confirm = function () {
        console.log($scope.args);
        var errors = validateObj();
        if (errors.length > 0) {
            errorModal.open(errors);
            return;
        }
        loading.open("", ".addIPPool");
        ipPoolService.create_ip_pool({}, $scope.args, function (res) {
            loading.close(".addIPPool");
            if (res.result) {
                $modalInstance.close(res.data);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };

    // $scope.exclude_ip_list = [{
    //     index: 1,
    //     ip: ""
    // }];
    $scope.add_interval = function () {
        var index_max = $scope.args.interval_list[$scope.args.interval_list.length - 1].index + 1;
        $scope.args.interval_list.push({
             index: index_max,
            ip_start: "",
            ip_end: ""
        })
    };
    $scope.minus_interval = function (row) {
        if ($scope.args.interval_list.length == 1) {
            return
        }
        for (var j = 0; j < $scope.args.interval_list.length; j++) {
            if ($scope.args.interval_list[j].index == row.index) {
                $scope.args.interval_list.splice(j, 1);
                return
            }
        }
    };

    $scope.add_list = function () {
        var index_max = $scope.args.excute_range[$scope.args.excute_range.length - 1].index + 1;
        $scope.args.excute_range.push({
            index: index_max,
            ip_start: "",
            ip_end:''
        })
    };

    $scope.minus_list = function (row) {
        if ($scope.args.exclude_ip_list.length == 1) {
            return
        }
        for (var j = 0; j < $scope.args.exclude_ip_list.length; j++) {
            if ($scope.args.exclude_ip_list[j].index == row.index) {
                $scope.args.exclude_ip_list.splice(j, 1);
                return
            }
        }
    };


    var validateObj = function () {
        var errors = [];
        if ($scope.args.title === "") {
            errors.push("名称不能为空！");
        }
        if ($scope.args.ip_net === "") {
            errors.push("网段不能为空！");
        }
        if ($scope.args.mask === "") {
            errors.push("掩码不能为空！");
        }
        if ($scope.args.gateway === "") {
            errors.push("网关不能为空！");
        }
        else {
            var tmp = $scope.args.ip_net.split("/");
            if (tmp.length != 2) {
                errors.push("网段格式有误!");
            }
            else {
                if (!CWApp.isIP(tmp[0])) {
                    errors.push("网段格式有误!");
                }
                else if (!CWApp.isNum(tmp[1])) {
                    errors.push("网段格式有误!");
                }
                else if (tmp[1] < 0 || tmp[1] > 32) {
                    errors.push("网段格式有误!");
                }
            }
        };
        for (var i in $scope.args.exclude_ip_list) {
            if ($scope.args.exclude_ip_list[i].ip != "") {
                if (!CWApp.isIP($scope.args.exclude_ip_list[i].ip)) {
                    errors.push("要排除的IP格式有误!");
                    return errors
                }
            }
        };
        for (var i = 0; i < $scope.args.interval_list.length; i++) {
            if ($scope.args.interval_list[i].ip_start == "" || $scope.args.interval_list[i].ip_end == "") {
                errors.push("区间不能为空！");
            }
        };
        return errors;
    }
}]);