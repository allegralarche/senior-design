'use strict';

var CFControllers = angular.module('CFControllers', []); // this is the app

CFControllers.controller('HomeCtrl', ['$scope',
	function($scope) {

		$scope.map = { center: { latitude: 45, longitude: -73 }, zoom: 8 };
		
	}]);

CFControllers.controller('TwitterCtrl', function($scope) {
	


});

module.exports = CFControllers;

