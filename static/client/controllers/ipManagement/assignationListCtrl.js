controllers.controller('assignationListCtrl', ["$scope", "ipService", "loading", "errorModal", function ($scope, ipService, loading, errorModal) {
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

    // $scope.detectIPs = function () {
    //     var errors = validate();
    //     if (errors.length > 0) {
    //         errorModal.open(errors);
    //         return;
    //     }
    //     loading.open();
    //     ipService.detect_ips({
    //         ips: $scope.filterObj.ips,
    //         ip_type: $scope.filterObj.ip_type,
    //         start_ip: $scope.filterObj.start_ip,
    //         end_ip: $scope.filterObj.end_ip
    //     }, {}, function (res) {
    //         loading.close();
    //         if (res.result) {
    //             $scope.result_list = res.data;
    //             $scope.flag = "00";
    //         }
    //         else
    //             errorModal.open(res.data);
    //     })
    // };

    $scope.gridOptions = {
        data: "result_list",
        columnDefs: [
            {field: "ip", displayName: "IP地址"}
        ]
    };

    var validate = function () {
        var errors = [];
        if ($scope.filterObj.ip_type == "00") {
            var ip_list = $scope.filterObj.ips.split(",");
            for (var i = 0; i < ip_list.length; i++) {
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
            if (!CWApp.isIP($scope.filterObj.end_ip)) {
                errors.push("结束IP格式不正确！");
            }
        }
        return errors;
    }
}]);