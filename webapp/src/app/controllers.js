'use strict';

var Twitter = require('twitter-node-client').Twitter;
var $ = require("jquery");

var CFControllers = angular.module('CFControllers', []); // this is the app
// callback function
var error = function (err, response, body) {
        console.log('ERROR [%s]', err);
    };

// Home Controller
CFControllers.controller('HomeCtrl', ['$scope',
	function($scope) {
		
	}]);

<<<<<<< HEAD
CFControllers.controller('TwitterCtrl', function($scope) {
	$scope.getTweets = function() {
		twitterClient.getUserTimeline({screen_name: $scope.username, count : 10}, error, function(data) {
			console.log(data);
=======
// Map Controller
CFControllers.controller('MapCtrl', ['$scope',
	function($scope) {
		$scope.map = { center: { latitude: 45, longitude: -73 }, zoom: 8 };
	}])

// Twitter User Controller
CFControllers.controller('TwitterCtrl', function($scope, $q, twitterService) {
	$scope.tweets = [];

	twitterService.initialize();

	$scope.refreshTimeline = function(maxID) {
		twitterService.getLatestTweets(maxID).then(function(data) {
			$scope.tweets = $scope.tweets.concat(data);

			for (var t in $scope.tweets) {
				console.log(t);
			}
		}, function() {
			$scope.rateLimitError = true;
>>>>>>> d2cbb8b8ac0c8be9f2944a1ced280cebd57e5490
		});
	}

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

