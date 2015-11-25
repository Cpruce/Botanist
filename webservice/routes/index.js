var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'Botanist' });
});

router.get('/signatures.json', function(req, res) {
    //res.setHeader('Content-Type', 'application/json');
    res.sendFile('/home/cory/School/Semester4/MobSec/Project/Botanist/webservice/signatures.json');
    //res.send(JSON.parse(fs.readFileSync('signatures.json', 'utf8'))); 	
    //res.render('add', {title: 'Add a Wesource'});
});

router.get('/img/botanist.png', function(req, res) {
    //res.setHeader('Content-Type', 'application/json');
    res.sendFile('/home/cory/School/Semester4/MobSec/Project/Botanist/webservice/views/botanist.png');
    //res.send(JSON.parse(fs.readFileSync('signatures.json', 'utf8'))); 	
    //res.render('add', {title: 'Add a Wesource'});
});

module.exports = router;
