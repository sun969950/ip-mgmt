controllers.controller('error', ["$scope", "$modalInstance", "errorList", function ($scope, $modalInstance, errorList) {
    $scope.errors = errorList;
    $scope.confirm = function () {
        $modalInstance.close();
    };
}]);