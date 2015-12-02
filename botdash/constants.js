function define(name, value) {
	Object.defineProperty(exports, name, {
		value: value,
		enumerable: true 
	});
}

// MongoDB collections
define('USER', 'user');
define('HOMEHUBS', 'homehubs');
define('HHSTATUS', 'hhstatus');

// HTTP Response Code
define('SUCCESS', 200);
define('NOT_EXIST', 404);
define('INTERNAL_ERROR', 500);