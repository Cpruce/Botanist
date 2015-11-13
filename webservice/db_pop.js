/* Cory Pruce 
 *
 * Script to populate 
 * the database upon
 * initialization
 *
 * */

conn = new Mongo();
db = connect("WeSourceDB");

// clear collections if already exist
db.users.remove({});
db.wesources.remove({});

db.users.insert({'surname' : 'Cpruce','email' : 'corypruce@test.com','givenName' : 'Cory Pruce', 'password': 'a13raKadabra', 'age' : 23,'location' : 'Sunnyvale','gender' : 'Male'});
db.users.insert({'surname' : 'test1','email' : 'test1@test.com','givenName' : 'Kevin Chang','password': 'a13raKadabra','age' : 27,'location' : 'San Francisco','gender' : 'Male'});
db.users.insert({'surname' : 'test2','email' : 'test2@test.com','givenName' : 'Aaron Nozaki','password': 'a13raKadabra','age' : 27,'location' : 'San Francisco','gender' : 'Male'});
db.users.insert({'surname' : 'test3','email' : 'test3@test.com','givenName' : 'Kevin Tong','password': 'a13raKadabra','age' : 21,'location' : 'San Francisco','gender' : 'Male'});


// RNR

db.wesources.insert({'wesource' : 'HP PA Pool Table', 'type': 'rnr', 'time_limit' : '12:27', 'max': 4, 'location' : 'Gameroom','availability' : 4, 'img': 'pool.jpg'});
db.wesources.insert({'wesource' : 'HP PA Pingpong Table', 'type': 'rnr', 'time_limit' : '12:27', 'max': 4, 'location' : 'Gameroom','availability' : 4, 'img': 'pingpong.jpg'});
db.wesources.insert({'wesource' : 'Basketball', 'type': 'rnr',  'max': 10, 'location' : 'Gameroom','availability' : 1, 'img':'basketball.jpg'});
db.wesources.insert({'wesource' : 'Road Bike', 'type': 'rnr', 'time_limit' : '12:27','max': 1, 'location' : 'Bike or Hike','availability' : 1, 'img': 'bike.jpg'});
db.wesources.insert({'wesource' : 'Meme', 'type': 'rnr', 'time_limit' : '12:27', 'max': 4, 'location' : 'Gameroom','availability' : 1, 'img':'c2c.png'});

// Parking
db.wesources.insert({'wesource' : 'HP PA Near Parking Lot','type': 'parking', 'location' : 'HP PA Parking lot','availability' : 5, 'max' : 30, 'img':'parking1.jpeg' });
db.wesources.insert({'wesource' : 'Section A Parking','type': 'parking', 'location' : 'Levi Stadium Parking lot','availability' : 4, 'max' : 50, 'img':'parking2.jpeg' });
db.wesources.insert({'wesource' : 'Parking Spots','type': 'parking', 'location' : 'Morse Ave','availability' : 3, 'max' : 3, 'img':'parking3.jpg' });
db.wesources.insert({'wesource' : 'Parking','type': 'parking', 'location' : 'Side of Dorm','availability' : 2, 'max' : 0, 'img':'parking4.jpeg' });

// Other

db.wesources.insert({'wesource' : 'bagels','type':'other', 'location' : 'Breakroom','availability' : 10, 'max': 12, 'img': 'bagels.jpg'});
db.wesources.insert({'wesource' : 'Dorm Laundry Unit','type':'other', 'location' : 'Atherton Hall','availability' : 2, 'max': 5, 'img': 'laundry.jpg'});
db.wesources.insert({'wesource' : 'Meeting Room','type':'other', 'location' : 'HP Building 5','availability' : 0, 'max': 1, 'img': 'room1.jpg'});
db.wesources.insert({'wesource' : 'Conference Room','type':'other', 'location' : 'HP Building 20','availability' : 1, 'max': 1, 'img': 'room2.jpg'});

// Accessories

db.wesources.insert({'wesource' : 'laptop','type':'appliances', 'location' : 'mobile','availability' : 1, 'max': 1, 'img': 'laptop.jpg'});
db.wesources.insert({'wesource' : 'WeSource Source Code','type':'appliances', 'location' : 'mobile','availability' : 1, 'max': 1, 'img': 'source.jpg'});




