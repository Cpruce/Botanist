var express = require('express');

var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var fs = require('fs');

var app = express();
var DATA_FILE = path.join(__dirname, '/public/data.json');
var OLD_DATA_FILE = path.join(__dirname, '/public/data_initial.json');  
// MongoDB wrapper
var mongo = require('./mongo');
// Used when query collection by _id field
var ObjectId = require('mongodb').ObjectID;
// Constants used in this application
var constants = require('./constants');

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(express.static(path.join(__dirname, 'public')));
app.get('/', function(req, res) {
    res.sendfile('./public/index.html');
});


/**
* REST APIs for other applications to feed/retrieve homehub
* status
*/

/**
*  Register a new homehub to the cloud controller.
*  Return the uuid of the new homehub
*/
app.post('/api/registerhh', function(req, res) {
  var hh = {};
  mongo.insertOne(constants.HOMEHUBS, hh, function (err, result) {
    if(err != null) {
      internalError(res, err);
    } else {
      res.status(constants.SUCCESS).send({'uid' : hh._id});
    }
  });
});

/**
* List all the homehub configurations
*/
app.get('/api/listhhs', function(req, res) {
  mongo.query(constants.HOMEHUBS, {}, function(err, docs) {
    if(err != null) {
      internalError(res, err);
    } else {
      res.status(constants.SUCCESS).send(docs);
    }
  });
});

/**
* Retrieve specifc homehub configuration
*/
app.get('/api/hhinfo', function(req, res) {
  mongo.query(constants.HOMEHUBS, {'_id': new ObjectId(req.query.uid)},
    function(err, docs) {
      if(err != null) {
        internalError(res, err);
      } else {
        var doc = {};
        if(docs.length > 0) {
          doc = docs[0];
        }
        res.status(constants.SUCCESS).send(doc);
      }
    });
});

/**
* Update the homehub information, which includes the name, 
* longitude, latitude and the device list
*/
app.post('/api/hhinfo', function(req, res) {
  mongo.update(constants.HOMEHUBS, {'_id': new ObjectId(req.body.uid)},
    {$set: req.body.info}, function(err, result) {
      if(err != null) {
        internalError(res, err);
      } else {
        res.status(constants.SUCCESS).send('');
      }
    });
});

/**
* Feed the homehub status
*/
app.post('/api/hhstatus', function(req, res) {
  mongo.insertOne(constants.HHSTATUS, req.body,
    function(err, result) {
      if(err != null) {
        internalError(res, err);
      } else {
        res.status(constants.SUCCESS).send('');
      }
    });
});

/**
  Get the price for a specific homehub
*/
app.get('/api/price', function(req, res) {
  mongo.query(constants.HOMEHUBS, {'_id': new ObjectId(req.query.uid)},
    function(err, docs) {
      if(err != null || docs.length == 0) {
        internalError(res, err);
      } else {
        res.status(constants.SUCCESS).send({'price':docs[0].price});
      }
    });
});

/**
* Set the price for a specific homehub
*/
app.post('/api/price', function(req, res) {
  mongo.update(constants.HOMEHUBS, {'_id': new ObjectId(req.body.uid)},
    {$set: {'price' : req.body.price}}, function(err, result) {
      if(err != null) {
        internalError(res, err);
      } else {
        res.status(constants.SUCCESS).send('');
      }
    });
});

app.get('/api/aggregate_price', function(req, res) {

  var rnum
  var tsNow = Date.now();
   
  fs.readFile(DATA_FILE, function(err, data) {
    if (err) {
      console.error(err);
      process.exit(1);
    }
    
    var price_histories = JSON.parse(data);    

    for (var i = 0; i < price_histories.length; i++){
        rnum = Math.round(Math.random(0, 81)*100);
        price_histories[i].values.push([tsNow, rnum]);
    
    }

    fs.writeFile(DATA_FILE, JSON.stringify(price_histories), function(err, data2){
        if (err) {
            console.error(err);
            process.exit(1);
        }

        res.setHeader('Cache-Control', 'no-cache');
        res.json(price_histories);
 
    }); 
    
  });
});


/**
* Helper function to return internal error message
* to the web client.
* @param res - The Http Response object
* @param err - The error object
* @return void
*/
function internalError(res, err) {
  console.warn(err);
  res.status(constants.INTERNAL_ERROR).send('Internal Error');
}

app.get('/api/data', function(req, res) {
  
  fs.readFile(OLD_DATA_FILE, function(err, data) {
    if (err) {
      console.error(err);
      process.exit(1);
    }
   
    res.setHeader('Cache-Control', 'no-cache');
    res.json(JSON.parse(data));
  });
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});

//app.listen(3000);
mongo.init(function() {
  app.listen(3000, function() {

    fs.writeFile(DATA_FILE, JSON.stringify([{"key":"Slac","values":[]}, {"key":"CMU sv", "values":[]}, {"key":"Yizhe Home","values":[]},{"key": "Cory Home", "values":[]}]), function(err, data2){
        if (err) {
            console.error(err);
            process.exit(1);
        }

        console.log('Rewrote ' + DATA_FILE);
    });   
    console.log("Node app is running at localhost:" + 3000)
  })  
})
//module.exports = app;
