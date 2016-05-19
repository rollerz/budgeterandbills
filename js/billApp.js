var billApp = angular.module('billApp', ['ngRoute']);

/* CUSTOM DELIMITER NOTATION FOR ANGULAR FROM STACKOVERFLOW */
/* NOTE: See Credits Page for more detail */
/* TODO: Credits Page */
billApp.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

billApp.controller('IndexCtrl', function($scope, $routeParams, $http) {
    //TODO: run a class in main.py
});

billApp.controller('NewBillCtrl', function($scope, $routeParams, $http) {
    $scope.billSubmit = function() {
        console.log("Form function ran!");
        $http.post('/newBill').then(
            function() {
                console.log("Success!")
                window.location.assign("#/success");
            },
            function() {
                console.log("Failure!")
            });
    }
});

billApp.controller('UpdateCtrl', function($scope, $routeParams, $http) {
    //TODO: run a class in main.py
});

// billApp.controller('SuccessCtrl', function($scope, $routeParams, $http) {
//     // $http.get('/newBill');
// });

billApp.controller('BillsListCtrl', function($scope /*TODO: ARRAY HERE */) {
    // states.list(function(states) {
    //     $scope.states = states;
    // });
});

billApp.controller('BillDetailCtrl', function($scope, $routeParams /*TODO: ARRAY HERE */) {
    // states.find($routeParams.stateAbrv, function(state) {
    //     $scope.state = state;
    // });
    // reps.list(function(reps) {
    //     $scope.reps = reps;
    // });
});

//---- FILTERS ----//

billApp.filter('encodeURI', function() {
    return function(x) {
        return encodeURIComponent(x);
    };
});

// billApp.filter('repeat', function() {
//     return function(x) {
//         return x.split("ly", 1);
//     }
// });

// $http({method: 'POST', url: '/newBill', data: my_data}).
//     success(function(data, status, headers, config) {
//         // this callback will be called asynchronously
//         // when the response is available
//     }).
//     error(function(data, status, headers, config) {
//         // called asynchronously if an error occurs
//         // or server returns response with an error status.
//     });

// $http.get('/newBill');
