'use strict';

var Twitter = require('twitter-node-client').Twitter;
var CFControllers = angular.module('CFControllers', []); // this is the app

var twitterConfig = {
        "consumerKey": "3vDKSh6NkZD5TYe4YSra5Vlws",
        "consumerSecret": "2mJOtdrtaAzEsBcRCHBeCIaqbJaReF5IZS8zjEZTAliQiASh5D",
        "accessToken": "363448613-TPHWxpzk69qJ4JbwOMeCORXucgB40Oq9bJxoKIBL",
        "accessTokenSecret": "k9NpfGnrGLjBtui2Ay7E3kC7JDeC5sO1g6BWrouL2CbNr",
        "callBackUrl": ""
    }

var twitterClient = new Twitter(twitterConfig);
// callback function
var error = function (err, response, body) {
        console.log('ERROR [%s]', err);
    };

CFControllers.controller('HomeCtrl', ['$scope',
	function($scope) {

		$scope.map = { center: { latitude: 45, longitude: -73 }, zoom: 8 };
		
	}]);

CFControllers.controller('TwitterCtrl', function($scope) {
	$scope.getTweets = function() {
		twitterClient.getUserTimeline({screen_name: $scope.username, count : 10}, error, function(data) {
			console.log(data);
		});
	};


});

module.exports = CFControllers;

