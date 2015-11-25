/* Cory Pruce 
 *
 * Script to populate 
 * the database upon
 * initialization
 *
 * */

conn = new Mongo();
db = connect("BotanistDB");

// clear collections if already exist
/*db.users.remove({});
db.wesources.remove({});

db.users.insert({'surname' : 'Cpruce','email' : 'corypruce@test.com','givenName' : 'Cory Pruce', 'password': 'a13raKadabra', 'age' : 23,'location' : 'Sunnyvale','gender' : 'Male'});
db.users.insert({'surname' : 'test1','email' : 'test1@test.com','givenName' : 'Kevin Chang','password': 'a13raKadabra','age' : 27,'location' : 'San Francisco','gender' : 'Male'});
db.users.insert({'surname' : 'test2','email' : 'test2@test.com','givenName' : 'Aaron Nozaki','password': 'a13raKadabra','age' : 27,'location' : 'San Francisco','gender' : 'Male'});
db.users.insert({'surname' : 'test3','email' : 'test3@test.com','givenName' : 'Kevin Tong','password': 'a13raKadabra','age' : 21,'location' : 'San Francisco','gender' : 'Male'});
*/




