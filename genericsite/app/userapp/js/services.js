'use strict';

/* Services */

var userServices = angular.module('userServices', ['ngResource']);

userServices.factory('User', ['$resource',
  function($resource){
    return $resource('/siteusers/:action', {}, {
      all: {method:'POST', params: {action: 'all'}, isArray:true},
      view: {method:'POST', params: {action: 'view'}, isArray:false},
      add: {method:'POST', params: {action: 'add'}, isArray:false},
      update: {method:'POST', params: {action: 'update'}, isArray:false},
      delete: {method:'POST', params: {action: 'delete'}, isArray:false}
    });
  }]);
