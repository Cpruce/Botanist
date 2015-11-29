var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var fs = require('fs');

var app = express();
var DATA_FILE = path.join(__dirname, '/public/data.json');

var mongo = require('./mongo.js');

app.set('views', __dirname + '/views');
app.set('view engine', 'jsx');
app.engine('jsx', require('express-react-views').createEngine());

// view engine setup
//app.set('view', path.join(__dirname, 'views'));
//app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));

//app.use('/', express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public')));
app.get('/', function(req, res) {
    //res.sendfile('./public/index.html');

    var initialState = {
    items: [
      'document your code',
      'drop the kids off at the pool',
      '</script><script>alert(666)</script>'
    ],
    text: ''
  };
  res.render('Html', { data: initialState }); 

});

app.get('/api/data', function(req, res) {
  mongo.query('homehubs', {}, function(err, results) {
    console.log(results[0]);
  });
  fs.readFile(DATA_FILE, function(err, data) {
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
    //console.log("Node app is running at localhost:" + 3000)
  })  
})
//module.exports = app;
