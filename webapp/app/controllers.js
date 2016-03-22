'use strict';

var CFControllers = angular.module('CFControllers', []);

CFControllers.controller('HomeCtrl', ['$scope',
	function($scope) {

		$scope.map = { center: { latitude: 45, longitude: -73 }, zoom: 8 };
		
	}]);

module.exports = CFControllers;

