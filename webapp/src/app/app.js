'use strict';

// Styles
require("../style/global.css");
require("bootstrap/dist/css/bootstrap.css");

var angular = require("angular");
var angularRoute = require("angular-route");
var angularSanitize = require("angular-sanitize");
var ngTweet = require("../../lib/ngTweet/ngtweet.min.js");
var logger = require("angular-simple-logger");
var angMaps = require("angular-google-maps");
var localStorage = require("angular-local-storage");

var services = require("./services");
var directives = require("./directives");
var controllers = require("./controllers");

var CFApp = angular.module("CFApp", [
	'ngRoute',
	'CFControllers',
	'CFDirectives',
	'CFServices',
	'ngSanitize',
	'ngtweet',
	'uiGmapgoogle-maps',
	'LocalStorageModule'
]);

CFApp.config(['uiGmapGoogleMapApiProvider',
	function(uiGmapGoogleMapApiProvider) {
		uiGmapGoogleMapApiProvider.configure({
			key: 'AIzaSyBPxhG-Mj99rpgKrC9y9RESEc-TOKLJd5s',
			v: '3.23',
			libraries: 'weather,geometry,visualization'
		})
	}]);