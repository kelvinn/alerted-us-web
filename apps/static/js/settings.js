var settingsEditApp = angular.module('settingsEditApp', ["xeditable", 'ui.bootstrap']);

settingsEditApp.config(['$httpProvider', '$interpolateProvider',
    function($httpProvider, $interpolateProvider) {
    /* for compatibility with django teplate engine */
    //$interpolateProvider.startSymbol('{$');
    //$interpolateProvider.endSymbol('$}');
    /* csrf */
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]);

settingsEditApp.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

var settingsEditCtrl = function ($scope, $http) {
    /* get location data list */
    $http({method: 'GET', url: vars.settingsUrl }).
        success(function (data, status, headers, config) {
            $scope.$root.loaded = true;
            $scope.data = data;
            //$scope.$broadcast('updateResults', data);
    });


    $scope.updateUser = function() {
        $http({method: 'PATCH', url: vars.settingsUrl, data: $scope.data}).
        success(function(data, status, headers, config) {
            $scope.data['success'] = true;
        }).
        error(function(data, status, headers, config) {
            $scope.data['success'] = false;
        });
        //return $http.post('/updateUser', {id: $scope.user.id, name: data});
    };

};