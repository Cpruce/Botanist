var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'WeSource' });
});

router.get('/signatures.json', function(req, res) {
    //res.setHeader('Content-Type', 'application/json');
    res.sendFile('/home/cory/School/Semester4/MobSec/Project/Botanist/webservice/signatures.json');
    //res.send(JSON.parse(fs.readFileSync('signatures.json', 'utf8'))); 	
    //res.render('add', {title: 'Add a Wesource'});
});

router.get('/img/:img', function(req, res){
	res.sendFile('/home/cory/WeSourceServer/public/images/' + req.params.img);	
});

module.exports = router;
