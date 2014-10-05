var alertsApp = angular.module('alertsApp', ["xeditable", 'ui.bootstrap', 'google-maps', 'ngAutocomplete']);

alertsApp.config(['$httpProvider', '$interpolateProvider',
    function($httpProvider, $interpolateProvider) {
    /* for compatibility with django teplate engine */
    //$interpolateProvider.startSymbol('{$');
    //$interpolateProvider.endSymbol('$}');
    /* csrf */
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';


}]);

alertsApp.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});


var alertsCtrl = function ($scope, $http) {

    $scope.map = {
        center: {
            latitude: -33,
            longitude: 151
        },
        coords: {
            latitude: -33,
            longitude: 151
        },
        zoom: 10
    };

};