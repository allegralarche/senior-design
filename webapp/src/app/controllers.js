'use strict';

var Twitter = require('twitter-node-client').Twitter;
var $ = require("jquery");
var _ = require("lodash");


var CFControllers = angular.module('CFControllers', []); // this is the app

// callback function
var error = function (err, response, body) {
    console.log('ERROR [%s]', err);
};

// Home Controller
CFControllers.controller('HomeCtrl', ['$scope',
	function($scope) {
		console.log("In home");
	}]);

// Map Controller
CFControllers.controller('MapCtrl', ['$scope',
	function($scope) {
		console.log("In Map");

		$scope.map = { 
			center: { 
				latitude: 45, 
				longitude: -73 
			}, 
			zoom: 8 
		};
	}]);

// Twitter User Controller
CFControllers.controller('TwitterCtrl', function($scope, $q, $http, twitterService, localStorageService) {
	$scope.tweets = [];
	twitterService.initialize();

	$scope.refreshTimeline = function(maxID) {
		console.log("getting tweets");
		twitterService.getLatestTweets(maxID).then(function success(data) { // returns array of tweet objects
			$http({
				method: "POST",
				url: "/filterTweets",
				data: {tweets : data}
			}).then(function success(response) {
				console.log("success");
				$scope.tweets = $scope.tweets.concat(data);
				localStorageService.set("tweets", $scope.tweets);
			}, function error(response) {
				console.log('error: ' + response.statusText);
			});
			
		}, function error() {
			$scope.rateLimitError = true;
		});
	};


	$scope.connectButton = function() {
		twitterService.connectTwitter().then(function() {
			if (twitterService.isReady()) {
				$('#connectButton').fadeOut(function() {
					$('#getTimelineButton, #signOut').fadeIn();
                    $scope.refreshTimeline();
                    $scope.connectedTwitter = true;
				});
			}
		});
	}

	$scope.signOut = function() {
		twitterService.clearCache();
		$scope.tweets.length = 0;
		$('#getTimelineButton, #signOut').fadeOut(function() {
			$('#connectButton').fadeIn();
			$scope.$apply(function() {
				$scope.connectedTwitter = false;
			})
		})
	}

	if (twitterService.isReady()) {
		$('#connectButton').hide();
		$('#getTimelineButton, #signOut').show();
        $scope.connectedTwitter = true;
        $scope.refreshTimeline();
	};



});

module.exports = CFControllers;

