controllers.controller("home", ["$scope", "siteService","errorModal","loading", function ($scope, siteService,errorModal,loading) {
    $scope.countObj = {};
    $scope.userIpList = [];
    $scope.change_list = [];
    $scope.ipUsedReports = {
        data: "userIpList",
        title: {text: 'IP使用情况统计', enabled: true},
        unit: "个",
        size: "250px"
    };

    $scope.logReports = {
        data: "change_list",
        chart: {type: 'line'},
        title: {text: '近期的变动IP数（10天）', enabled: true},
        yAxis: {
            allowDecimals: true,
            title: {
                text: '变动IP数'
            }
        },
        xAxis: {
            categories: []
        },
        //提示框位置和显示内容
        tooltip: {
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:f}</b></td></tr>',
            headerFormat: ""
        }
    };
    loading.open();
    siteService.get_count_obj({}, {}, function (res) {
        loading.close();
        if (res.result) {
            $scope.countObj = res.data;
            $scope.userIpList = res.userIpList;
            $scope.logReports.xAxis.categories = res.categories;
            $scope.change_list = res.change_list;
        }
        else{
            errorModal.open(res.data)
        }
    })

}]);
