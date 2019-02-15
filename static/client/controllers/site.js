controllers.controller("site", ["$scope", function ($scope) {
    $scope.menuList = [
        {
            displayName: "首页", iconClass: "fa fa-home fa-lg", url: "#/home"
        },
        // {
        //     displayName: "申请管理", iconClass: "fa fa fa-bookmark-o fa-lg",
        //     children: [
        //         {displayName: "未完申请", url: "#/applyList"},
        //         {displayName: "已完申请", url: "#/completedApply"}
        //     ]
        // },
        {
            displayName: "IP管理", iconClass: "fa fa-align-left fa-lg fa18",
            children: [
                {displayName: "资源池管理", url: "#/ipPoolList"},
                {displayName: "排除IP", url: "#/excludeIP"},
                {displayName: "已用IP", url: "#/segmentManagement"},
                // {displayName: "分配未使用IP", url: "#/subjectsegMange"},
                {displayName: "可用IP", url: "#/usableIP"},
                {displayName: "IP查询", url: "#/assignationList"},
                {displayName: "分配IP", url: "#/ipAllocation"},
                {displayName: "全局IP", url: "#/ipAll"},
            ]
        },
        {
            displayName: "系统管理", iconClass: "fa fa-cog fa-lg",
            children: [
                // {displayName: "邮箱管理", url: "#/mailManagement"},
                {displayName: "操作日志", url: "#/operationLog"}
            ]
        }
    ];

    $scope.menuOption = {
        data: 'menuList',
        locationPlaceHolder: '#locationPlaceHolder',
        adaptBodyHeight: CWApp.HeaderHeight + CWApp.FooterHeight
    };

    $scope.goToUrl = function (page) {
        window.location.href = "#/" + page;
    };

    $scope.isVisit = function (url) {
        var urls = window.location.href.split("#/");
        if (urls.length == 1) {
            if (url == "ipApply") {
                return true;
            }
        }
        if (urls[1] == url) {
            return true;
        }
        return false;
    }

    //
    // $scope.goToUser = function () {
    //     window.open(site_url + "user/");
    // }
}]);