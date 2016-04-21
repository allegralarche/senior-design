
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const sshTunnel = require('tunnel-ssh');
const fs = require('fs')

const pythonShell = require('python-shell');


// need bodyParser for post requests 
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

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



app.post('/getPercents', function response(req, res) {
	var coords = [];

	var contents = fs.readFileSync('../python/counterfactuals.txt').toString().split("\n");
	for (var i = 0; i < contents.length; i++) {
		var line = contents[i];

		if (line == '') {
			continue;
		}

		var latitude = line.split(",")[0];
		var longitude = line.split(",")[1];

		if (latitude.indexOf("u'") > -1) {
			latitude = latitude.substring(3);
		}
		else {
			latitude = latitude.substring(1);
		}

		if (longitude.indexOf("u'") > -1) {
			longitude = longitude.substring(3, longitude.length - 2);
		}
		else {
			longitude = longitude.substring(1, longitude.length - 1);
		}
  		
		coords.push({latitude, longitude});
	}

	res.send(coords);

	/*var config = {
		host: '128.91.79.105',
		username: 'joeraso',
		dstPort: 3306,
		localPort: 3306,
		privateKey:require('fs').readFileSync('/Users/joeraso/.ssh/id_rsa')
	};

	var server = sshTunnel(config, function (error, result) {
		console.log(req.body);
		var pythonOptions = {
			scriptPath: '../python',
			args: [req.body.county, req.body.timeOne, req.body.timeTwo]
		}
		pythonShell.run('joeyScript.py', pythonOptions, function(err, results) {
			if(err) {
				throw err;
			}
			else {
				res.send(results[0]); // just a percentage
			}
		});
	});*/
});


app.listen(3000, '0.0.0.0', function (err) {
  if (err) {
    console.log(err);
  }
});
