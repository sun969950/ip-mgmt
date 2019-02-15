controllers.controller("ipDetectionCtrl", ["$scope", "loading", "ipService","errorModal", function ($scope, loading, ipService,errorModal) {
    $scope.filterObj = {
        ip_type: "00",
        ips: "",
        start_ip: "",
        end_ip: ""
    };

    $scope.flag = "";

    $scope.result_list = [];

    $scope.searchIPs = function () {
        var errors = validate();
        if (errors.length > 0) {
            errorModal.open(errors);
            return;
        }
        loading.open();
        ipService.allocation_search({
            ips: $scope.filterObj.ips,
            ip_type: $scope.filterObj.ip_type,
            start_ip: $scope.filterObj.start_ip,
            end_ip: $scope.filterObj.end_ip
        }, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.result_list = res.data;
                $scope.flag = "01";
            }
            else
                errorModal.open(res.data);
        })
    };

    var validate = function () {
        var errors = [];
        if ($scope.filterObj.ip_type == "00") {
            var ip_list = $scope.filterObj.ips.split(",");
            for (var i = 0; i < ip_list.length; i++) {
                if (ip_list[i] == "") {
                    errors.push("IP地址不能是空的！");
                    break;
                }
                if (!CWApp.isIP(ip_list[i])) {
                    errors.push(ip_list[i] + "的IP地址格式不正确！");
                    break;
                }
            }
        }
        else {
            if (!CWApp.isIP($scope.filterObj.start_ip)) {
                errors.push("起始IP格式不正确！");
            }
            else if ($scope.filterObj.start_ip == "") {
                errors.push("起始IP地址不能是空的！")
            }
            if (!CWApp.isIP($scope.filterObj.end_ip)) {
                errors.push("结束IP格式不正确！");
            }
            else if ($scope.filterObj.end_ip == "") {
                errors.push("结束IP地址不能是空的！")
            }
        }
        return errors;
    }
}]);