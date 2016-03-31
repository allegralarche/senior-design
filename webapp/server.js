
const path = require('path');
const express = require('express');

const webpack = require('webpack');
const webpackMiddleware = require('webpack-dev-middleware');
const webpackHotMiddleware = require('webpack-hot-middleware');
const config = require('./webpack.config.js');

const mysql = require('mysql');
const sshTunnel = require('tunnel-ssh');
const Twitter = require('twitter');

var ENV = process.env.npm_lifecycle_event;
var isTest = ENV === 'test'

const isDeveloping = process.env.NODE_ENV !== 'production';
const port = isDeveloping ? 3000 : process.env.PORT;
const app = express();


if (isDeveloping) {
	const compiler = webpack(config);
	const middleware = webpackMiddleware(compiler, {
	    publicPath: config.output.publicPath,
	    contentBase: 'src',
	    stats: {
	      colors: true,
	      hash: false,
	      timings: true,
	      chunks: false,
	      chunkModules: false,
	      modules: false
	    }
	});

	app.use(middleware);
	app.use(webpackHotMiddleware(compiler));
	app.get('*', function response(req, res) {
	    res.write(middleware.fileSystem.readFileSync(path.join(__dirname, 'dist/index.html')));
	    res.end();
	});


	const sshConfig = {
		host: '128.91.79.105',
		dstPort: 3306,
	    username: 'joeraso',
	    agent : process.env.SSH_AUTH_SOCK,
	    privateKey:require('fs').readFileSync('/Users/joeraso/.ssh/id_rsa')
	} 

	var server = sshTunnel(sshConfig, function (error, result) {
        //you can start using your resources here. (mongodb, mysql, ....) 
        var connection = mysql.createConnection({
		  host     : 'localhost',
		  user     : 'root',
		  password : '',
		  database : 'twitterGH'
		});
		connection.connect();

		connection.query('SELECT * FROM messages_en_coordstate WHERE coordinates IS NOT NULL LIMIT 10', function(err, rows, fields) {
		  if (err) {
			console.log("error");
			throw err;
		  }

		  console.log('The symbol is: ', rows);
		});

		connection.end();
    });

	var client = new Twitter({
		consumer_key: '	3vDKSh6NkZD5TYe4YSra5Vlws',
		consumer_secret: '	2mJOtdrtaAzEsBcRCHBeCIaqbJaReF5IZS8zjEZTAliQiASh5D',
		access_token_key: '363448613-TPHWxpzk69qJ4JbwOMeCORXucgB40Oq9bJxoKIBL',
		access_token_secret: 'k9NpfGnrGLjBtui2Ay7E3kC7JDeC5sO1g6BWrouL2CbNr'
	});

	

}
else {
  app.use(express.static(__dirname + '/dist'));
  app.get('*', function response(req, res) {
    res.sendFile(path.join(__dirname, 'dist/index.html'));
  });
}




app.listen(port, '0.0.0.0', function (err) {
  if (err) {
    console.log(err);
  }
  console.info('==> 🌎 Listening on port %s. Open up http://0.0.0.0:%s/ in your browser.', port, port);
});
