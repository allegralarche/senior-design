'use strict';

var Twitter = require('twitter-node-client').Twitter;
var PythonShell = require('python-shell');
var $ = require("jquery");

var CFControllers = angular.module('CFControllers', ['ngtweet']); // this is the app
// callback function
var error = function (err, response, body) {
        console.log('ERROR [%s]', err);
    };

// Home Controller
CFControllers.controller('HomeCtrl', ['$scope',
	function($scope) {
		
	}]);

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

		}, function() {
			$scope.rateLimitError = true;
		});
	}

	$scope.filterCounterfactuals = function(tweet) {
		var options = {
			args = [tweet.text],
			scriptPath = '../../../python/',
			pythonPath = 'C://Users/alleg/Anaconda2/python',
		};
		PythonShell.run('getCFFromTagged.py', options, function(err, result) {
			if(!err) {
				return result > 0;
			} else {
				console.log(err);
			}
		})
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

