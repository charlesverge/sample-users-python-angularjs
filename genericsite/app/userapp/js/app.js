'use strict';

/* App Module */

var usersApp = angular.module('usersApp', [
  'ngRoute',
  'userControllers',
  'xeditable',
  'ngCookies',
  'userServices'

]);

usersApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/users', {
        templateUrl: 'partials/user-list.html',
        controller: 'UserListCtrl'
      }).
      otherwise({
        redirectTo: '/users'
      });
  }]);

usersApp.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

usersApp.run( function run( $http, $cookies ){
    // For CSRF token compatibility with Django
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
})
