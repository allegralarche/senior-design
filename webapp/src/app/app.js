'use strict';

require("../style/global.css");
require("bootstrap/dist/css/bootstrap.css");

var angular = require("angular");
var angularRoute = require("angular-route");
var angularSanitize = require("angular-sanitize");
var controllers = require("./controllers");
var directives = require("./directives");
var services = require("./services");
var logger = require("angular-simple-logger");
var angMaps = require("angular-google-maps");

var CFApp = angular.module("CFApp", [
	'ngRoute',
	'CFControllers',
	'CFDirectives',
	'CFServices',
	'ngSanitize',
	'uiGmapgoogle-maps'
]);

CFApp.config(['uiGmapGoogleMapApiProvider',
	function(uiGmapGoogleMapApiProvider) {
		uiGmapGoogleMapApiProvider.configure({
			key: 'AIzaSyBPxhG-Mj99rpgKrC9y9RESEc-TOKLJd5s',
			v: '3.23',
			libraries: 'weather,geometry,visualization'
		})
	}]);