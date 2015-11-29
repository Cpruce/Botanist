var assert = require('assert');
var ObjectId = require('mongodb').ObjectID;
var MongoClient = require('mongodb').MongoClient;

var db
var url = 'mongodb://localhost:27017/PowernetDB';


// Query for one specific collection with condition. If conditioin is {},
// it will return all the document in that collection.
function query(collection, condition, callback) {
	db.collection(collection).find(condition).toArray(callback);
}

// Delete documents in the specified collection which meets the condition
function del(collection, condition, callback) {
	db.collection(collection).deleteMany(condition, callback);
}

// Insert one record into the specified collection
function insertOne(collection, record, callback) {
	db.collection(collection).insertOne(record, callback);
}

// Insert a bulk of of records into the specified collection
function insertBulk(collection, records, callback) {
	var batch = db.collection(collection).initializeUnorderedBulkOp();
	for(var i = 0; i < records.length; i++) {
		batch.insert(records[i]);
	}
	batch.execute(callback);
}

// Used to init the mongodb connection. db is used as a connection pool 
// to improve the performance. Make sure the node.js server is started in
// the callback function.
function init(callback) {
	MongoClient.connect(url, function(err, database) {
		assert.equal(null, err);
		db = database;
		callback();
	});
}

exports.init = init
exports.del = del
exports.query = query
exports.insertOne = insertOne
exports.insertBulk = insertBulk

/*
var mongo = require('./mongo.js')

app.get('/', function(request, response) {
	mongo.query('homehubs', {}, function(err, results) {
		response.send(results);
	});
})
*/
