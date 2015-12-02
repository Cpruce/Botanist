var assert = require('assert');
var MongoClient = require('mongodb').MongoClient;

var db
var url = 'mongodb://localhost:27017/PowernetDB';

/**
*	Query for one specific collection with condition. If conditioin is {},
*	it will return all the document in that collection.
*
*	@param	{String} collection - The name of the collection
*	@param	{JSON}	condition - The filtering condition
*	@param	{function} callback - The callback function
*	@return void
*/
function query(collection, condition, callback) {
	db.collection(collection).find(condition).toArray(callback);
}

/**
*	Delete documents in the specified collection which meets the condition
*
*	@param	{String} collection - The name of the collection
*	@param	{JSON}	condition - The filtering condition
*	@param	{function} callback - The callback function
*	@return void
*/
function del(collection, condition, callback) {
	db.collection(collection).deleteMany(condition, callback);
}

/**
*	Update documents in the specified collection which meets the condition
*
*	@param	{String} collection - The name of the collection
*	@param	{JSON}	condition - The filtering condition
*	@param	{JSON}	val - The value to be updated
*	@param	{function} callback - The callback function
*	@return void
*/
function update(collection, condition, val, callback) {
	db.collection(collection).updateOne(condition, val, callback);
}

/**
*	Insert one record into the specified collection
*
*	@param	{String} collection - The name of the collection
*	@param	{JSON}	record - The new record in JSON format
*	@param	{function} callback - The callback function
*	@return void
*/
function insertOne(collection, record, callback) {
	db.collection(collection).insertOne(record, callback);
}

/**
*	Insert a bulk of of records into the specified collection
*
*	@param	{String} collection - The name of the collection
*	@param	{Array}	records - A list of JSON records to be inserted
*	@param	{function} callback - The callback function
*	@return void
*/
function insertBulk(collection, records, callback) {
	var batch = db.collection(collection).initializeUnorderedBulkOp();
	for(var i = 0; i < records.length; i++) {
		batch.insert(records[i]);
	}
	batch.execute(callback);
}

/**
*	Used to init the mongodb connection. db is used as a connection pool
*	to improve the performance. Make sure the node.js server is started in
*	the callback function.
*
*	@param	{function} callback - The callback function
*	@return void
*/
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
exports.update = update
exports.insertOne = insertOne
exports.insertBulk = insertBulk

/**
*	One example of how to use the query function.	
*
*	var mongo = require('./mongo')
*
*	app.get('/', function(request, response) {
*		mongo.query('homehubs', {}, function(err, results) {
*			response.send(results);
*		});
*	})
*/
