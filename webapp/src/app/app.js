'use strict';

// Styles
require("../style/global.css");
require("../style/angularMaterial.css");
require("bootstrap/dist/css/bootstrap.css");

var angular = require("angular");
var angularRoute = require("angular-ui-router");
var angularSanitize = require("angular-sanitize");
var ngTweet = require("../../lib/ngTweet/ngtweet.min.js");
var logger = require("angular-simple-logger");
var angMaps = require("angular-google-maps");
var localStorage = require("angular-local-storage");
var angularAnimate = require("angular-animate")
var angularMessage = require("angular-messages");
var angularAria = require("angular-aria");
var angularMaterial = require("angular-material");


var services = require("./services");
var directives = require("./directives");
var controllers = require("./controllers");

var CFApp = angular.module("CFApp", [
	'CFControllers',
	'CFDirectives',
	'CFServices',
	'ngSanitize',
	'ngtweet',
	'uiGmapgoogle-maps',
	'LocalStorageModule',
	'ui.router',
	'ngMaterial',
	'ngMessages',
]);

CFApp.config(function(uiGmapGoogleMapApiProvider, $stateProvider, $urlRouterProvider, $locationProvider, $mdIconProvider) {

		// Define Routes
		$locationProvider.html5Mode({
		  enabled: true,
		  requireBase: false
		});
		$urlRouterProvider.otherwise('/');

		$stateProvider
			.state('home', {
				url: '/',
				template: require('./partials/home.html'),
				controller: 'HomeCtrl',
				controllerAs: 'Home'
			})
			.state('map', {
				url: '/map',
				template: require('./partials/maps.html'),
				controller: 'MapCtrl',
				controllerAs: 'Map'
			})
			.state('userTweets', {
				url: '/userTweets',
				template: require('./partials/userTweets.html'),
				controller: 'TwitterCtrl',
				controllerAs: 'Twitter'
			});

		uiGmapGoogleMapApiProvider.configure({
			key: 'AIzaSyBPxhG-Mj99rpgKrC9y9RESEc-TOKLJd5s',
			v: '3.23',
			libraries: 'weather,geometry,visualization'
		});

		


	});