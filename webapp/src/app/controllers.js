'use strict';

var Twitter = require('twitter-node-client').Twitter;
var dateFormat = require('dateformat');
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
CFControllers.controller('MapCtrl', ['$scope', '$http',
	function($scope, $http) {

		var today = new Date();

		// Start Date
		$scope.minStartDate = new Date(2012, 0, 0, 0, 0, 0, 0)
  		$scope.maxStartDate = new Date(2015, 0, 0, 0, 0, 0, 0)

  		// End Date
  		$scope.minEndDate = new Date(2012, 0, 0, 0, 0, 0, 0)
  		$scope.maxEndDate = new Date(2015, 0, 0, 0, 0, 0, 0)

  
  		$scope.states = [
	        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID",
	        "IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS",
	        "MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK",
	        "OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV",
	        "WI","WY"	      
	    ];

	    $scope.markers = []
		$scope.map = { 
			center: { 
				latitude: 42.4, 
				longitude: -76
			}, 
			zoom: 7 
		};

		$scope.getPercents = function() {

			$scope.endDate = new Date(
				$scope.endDate.getFullYear(),
				$scope.endDate.getMonth(),
				$scope.endDate.getDate() + 1);

			console.log($scope.startDate);
			console.log($scope.endDate);

			var timeOne = dateFormat($scope.startDate, 'yyyy-mm-dd HH:MM:ss');
			var timeTwo = dateFormat($scope.endDate, 'yyyy-mm-dd HH:MM:ss');

			$http({
				method: "POST",
				url: "http://localhost:3000/getPercents",
				data: {
					state: $scope.state,
					timeOne: timeOne,
					timeTwo: timeTwo
				}
			}).then(function success(response) { // response is object with fields one and two
				console.log("success:" + response.data);

				for (var i = 0; i < response.data.length; i++) {
					response.data[i].keyId = i;
					console.log(response.data[i]);
				}
				$scope.markers = response.data;
			}, function error(response) {
				console.log('error: ' + response.statusText);
			});
		};
	}]);

// Twitter User Controller
CFControllers.controller('TwitterCtrl', function($scope, $q, $http, twitterService, localStorageService) {

	$scope.tweets = [];
	twitterService.initialize();

	$scope.refreshTimeline = function(maxID) {
		console.log("getting tweets");
		$('#loading').show();
		twitterService.getLatestTweets(maxID).then(function success(data) { // returns array of tweet objects
			$http({
				method: "POST",
				url: "/filterTweets",
				data: {tweets : data}
			}).then(function success(response) {
				console.log("success");
				$('#loading').hide();
				$scope.tweets = $scope.tweets.concat(response.data);
				//localStorageService.set("tweets", $scope.tweets);
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

