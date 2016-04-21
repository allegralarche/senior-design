
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const webpack = require('webpack');
const webpackMiddleware = require('webpack-dev-middleware');
const webpackHotMiddleware = require('webpack-hot-middleware');
const config = require('./webpack.config.js');

const isDeveloping = process.env.NODE_ENV !== 'production';
const port = isDeveloping ? 8080 : process.env.PORT;
const app = express();

const pythonShell = require('python-shell');


// need bodyParser for post requests 
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.post('/filterTweets', function response(req, res) {
	var tweets = req.body.tweets; // array of tweet objects
	var messages = [];
	for(var i in tweets) {
		messages.push(tweets[i].text);
	}
	var pythonOptions = {
		scriptPath: '../python',
		args: messages
	}
	pythonShell.run('allegraScript.py', pythonOptions, function(err, results) {
		if(err) {
			throw err;
		}
		else {
			var tbr = [];
			for(var j in results) {
				if(results[j] > 0) {
					tbr.push(tweets[j]);
				}
			}
			res.send(tbr);
		}
	});
});


if (isDeveloping) {
	const compiler = webpack(config);
	const middleware = webpackMiddleware(compiler, {
	    publicPath: config.output.publicPath,
	    contentBase: './src',
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


	app.get('/api/runScript', function response(req, res) {
		console.log("Running Script");
		res.end();
	});

	app.get('/', function response(req, res) {
	    res.write(middleware.fileSystem.readFileSync(path.join(__dirname, 'dist/index.html')));
	    res.end();
	});	

}
else {

  app.use(express.static(__dirname + '/dist'));

   app.get('/api/runScript', function response(req, res) {
	console.log("Running Script");
  });

  app.get('/', function response(req, res) {
    res.sendFile(path.join(__dirname, 'dist/index.html'));
  });


}


app.listen(port, '0.0.0.0', function (err) {
  if (err) {
    console.log(err);
  }
  console.info('==> 🌎 Listening on port %s. Open up http://0.0.0.0:%s/ in your browser.', port, port);
});
