'use strict';

/* Controllers */

var userControllers = angular.module('userControllers', []);

userControllers.controller('UserListCtrl', ['$scope', 'User',
  function($scope, User) {
    //for add form
    $scope.user = {};
    //for list of users
    $scope.users = User.all({'key': 'access'});
    $scope.orderProp = 'first_name';

    $scope.user_add_submit = function () { console.log("user_add_submit"); }

    $scope.add = function (user) {
        if ($scope.user_add.$invalid) {
            $scope.user_add.dirty = true;
            console.log("invalid");
        } else {
            user.key = "access";
            User.add(user, function () { $scope.users = User.all({'key': 'access'}); $scope.user = {}; });
        }
    }

    $scope.delete = function (uuid) { 
        User.delete({key:'access', uuid:uuid} );
        $('#user'+uuid).hide();
    }

    $scope.validateEdit = function(editableForm,$data) {
    }

    $scope.saveUser = function(editableForm,useredit) {
        if (!editableForm.$invalid) {
            useredit.key = "access";
            return User.update(useredit);
        } else {
            return false;
        }
  };

  }]);

userControllers.controller('UserDetailCtrl', ['$scope', '$routeParams', 'User', '$http',
  function($scope, $routeParams, User, $http) {
    $scope.user = User.view({'key': 'access', 'uuid': $routeParams.uuid});
    $scope.saveUser = function() {
        $scope.user.key = "access";
        return User.update( $scope.user);
  };
}]);
