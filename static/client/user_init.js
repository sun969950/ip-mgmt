var app = angular.module("myApp", ['myController', 'utilServices', 'myDirective', 'ui.bootstrap', 'ui.router', 'webApiService', 'ngGrid']);
var controllers = angular.module("myController", []);
var directives = angular.module("myDirective", []);


app.config(["$stateProvider", "$urlRouterProvider", "$httpProvider",
    function ($stateProvider, $urlRouterProvider, $httpProvider) {
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
        $urlRouterProvider.otherwise("/ipApply");//默认展示页面
        $stateProvider.state('ipDetection', {
            url: "/ipDetection",
            controller: "ipDetectionCtrl",
            templateUrl: static_url + "client/views/user_pages/ipDetection.html"
        })
        .state('ipApply', {
            url: "/ipApply",
            controller: "ipApplyCtrl",
            templateUrl: static_url + "client/views/user_pages/ipApply.html"
        })
        .state('myIP', {
            url: "/myIP",
            controller: "myIPCtrl",
            templateUrl: static_url + "client/views/user_pages/myIP.html"
        })
    }])
;
