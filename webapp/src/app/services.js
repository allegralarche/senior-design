'use strict';

var OAuth = require('oauthio-web').OAuth;
var $ = require('jquery');

var CFServices = angular.module('CFServices', []);

CFServices.factory('twitterService', function($q) {
	var authorizationResult = false;

	return {
		initialize: function() {
			OAuth.initialize("qBQk0Pv2UEXWGcbiAuXIqO3-GEk", {
				cache: true
			});

			authorizationResult = OAuth.create("twitter");
		},
		isReady: function() {
			return authorizationResult;
		},
		connectTwitter: function() {
			var deferred = $q.defer();
			OAuth.popup('twitter', {
				cache: true
			}, function(error, result) {
				if (!error) {
					authorizationResult = result;
					deferred.resolve();
				} else {

				}
			});
			return deferred.promise;
		},
		clearCache: function() {
			OAuth.clearCache('twitter');
			authorizationResult = false;
		},
		getLatestTweets: function(maxID) {
			var deferred = $q.defer();
			var url = '/1.1/statuses/home_timeline.json';
			if (maxID) {
				url += '?max_id=' + maxID;
			}
			var promise = authorizationResult.get(url).done(function(data) {
				deferred.resolve(data);
			}).fail(function(err) {
				deferred.reject(err);
			})
			return deferred.promise;
		}
	}
})

module.exports = CFServices;