controllers.controller("Message", ["$scope", "msg", "$modalInstance", function ($scope, msg, $modalInstance) {
    $scope.msg = {text: msg};
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    }
}]);