/* Cory Pruce 
 *
 * Script to populate 
 * the database upon
 * initialization
 *
 * */

conn = new Mongo();
db = connect("PowernetDB");

// clear collections if already exist
db.users.remove({});
db.homehubs.remove({});

db.users.insert({
    'username' : 'Cpruce',
    'email' : 'corypruce@gmail.com', 
    'password': 'a13raKadabra'
});
db.users.insert({
    'username' : 'test1',
    'email' : 'test1@test.com',
    'password': 'sfdsd'
});
db.users.insert({
    'username' : 'test2',
    'email' : 'test2@test.com',
    'password': 'a13raKadabra'
});

db.homehubs.insert({
    'hub_id' : 'fdsaf', 
    'location' : 
        {
        'longitude': 37.410401, 
        'latitude': -122.060032
        }, 
    'devices' : { 
        'fan' : 'on',
        'inverter': 'on',
        'heater': 'on'
    } 
});
db.homehubs.insert({
    'hub_id' : 'asdf', 
    'location' : {
        'longitude': 37.4201052,
        'latitude': -122.2021446 
    },
    'devices' : { 
        'fan' : 'on',
        'inverter': 'on',
        'heater': 'on'
    }
});
