'use strict';

var angular = require("angular");
var angularRoute = require("angular-route");
var controllers = require("./controllers");
var directives = require("./directives");
var services = require("./services");
var logger = require("angular-simple-logger");
var angMaps = require("angular-google-maps");
var style = require("./appStyles");
var jss = require("jss");

var sheet = jss.createStyleSheet(style, {named: false}).attach();

var CFApp = angular.module("CFApp", [
	'ngRoute',
	'CFControllers',
	'CFDirectives',
	'CFServices',
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