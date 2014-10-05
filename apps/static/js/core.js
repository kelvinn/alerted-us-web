var locationsEditApp = angular.module('locationsEditApp', ["xeditable", 'ui.bootstrap', 'google-maps', 'ngAutocomplete']);

locationsEditApp.config(['$httpProvider', '$interpolateProvider',
    function($httpProvider, $interpolateProvider) {
    /* for compatibility with django teplate engine */
    //$interpolateProvider.startSymbol('{$');
    //$interpolateProvider.endSymbol('$}');
    /* csrf */
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';


}]);

locationsEditApp.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

var locationsEditCtrl = function ($scope, $http) {
    $scope.result = '';
    $scope.options = '';
    $scope.details = {
        geometry: {
            location: {
                k: '',
                A: ''
            }
        }
    };

    $scope.map = {
        center: {
            latitude: 1,
            longitude: 1
        },
        coords: {
            latitude: '',
            longitude: ''
        },
        zoom: 10
    };

    $scope.$watch('details.geometry.location', function(newLocation, oldLocation) {
        if (newLocation){
            $scope.map = {
                center : {
                    latitude: newLocation.lat(),
                    longitude: newLocation.lng()
                },
                coords: {
                    latitude: newLocation.lat(),
                    longitude: newLocation.lng()
                },
                zoom: 15
            }
        }
   });

    $scope.$watch('results', function(newResults, oldResults) {
        if (newResults) {
            alert("testing");
        }
    });

    $scope.$on("updateResults",function(d){
        alert(d);
      $scope.data.results = d;
    });

    $scope.data = {success: false};
    $scope.pressed = function() {
        alert("success");
    };

    /* get location data list */
    $http({method: 'GET', url: vars.locationsUrl}).
        success(function (data, status, headers, config) {
            $scope.$root.loaded = true;
            $scope.data.results = data;
            //$scope.$broadcast('updateResults', data);
        });

    $scope.createLocation = function(value) {

        var lat = $scope.details.geometry.location.lat();
        var lng = $scope.details.geometry.location.lng();
        $scope.newPoint = {
            name: $scope.details.formatted_address,
            source: "static",
            geom : {
                type: "Point",
                coordinates: [
                    parseFloat(lng),
                    parseFloat(lat)
                    ]
            }
        };

        $http({method: 'POST', url: vars.locationsUrl, data: $scope.newPoint}).
        success(function(data, status, headers, config) {
            $scope.data['success'] = true;
            $scope.data.results.push(data);
        }).
        error(function(data, status, headers, config) {
            $scope.data['success'] = false;
        });
        //return $http.post('/updateUser', {id: $scope.user.id, name: data});
    };

    $scope.updateMap = function(value) {
        $scope.map = {
            center: {
                latitude: value[1],
                longitude: value[0]
            },
            coords: {
                latitude: value[1],
                longitude: value[0]
            },
            zoom: 15
        }
    };

    $scope.deleteLocation = function(value, idx) {
        $http({method: 'DELETE', url: vars.locationsUrl + value.id + '/', data: value}).
        success(function(data, status, headers, config) {
            $scope.data['success'] = true;
            $scope.data.results.splice(idx, 1);
        }).
        error(function(data, status, headers, config) {
            $scope.data['success'] = false;
        });
        //return $http.post('/updateUser', {id: $scope.user.id, name: data});
    };

    $scope.updateLocation = function(value) {
        $http({method: 'PATCH', url: vars.locationsUrl + value.id + '/', data: value}).
        success(function(data, status, headers, config) {
            $scope.data['success'] = true;
        }).
        error(function(data, status, headers, config) {
            $scope.data['success'] = false;
        });
        //return $http.post('/updateUser', {id: $scope.user.id, name: data});
    };
};
