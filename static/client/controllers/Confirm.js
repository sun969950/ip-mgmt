controllers.controller('confirm', ["$scope", "$modalInstance", "options", function ($scope, $modalInstance, options) {
    $scope.text = options.text;

    $scope.confirm = function () {
        $modalInstance.close();
    };
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);