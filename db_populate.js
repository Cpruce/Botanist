/* Cory Pruce 
 *
 * Script to populate 
 * the database upon
 * initialization
 *
 * */

conn = new Mongo();
db = connect("BotanistDB");

// clear collections if already exist. 
// REMOVE after adding actual data
db.users.remove({});
db.clusters.remove({});

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

db.clusters.insert({
    'so_file_name' : 'monodroid', 
    'apks_found_in' : ['XamarinHelloWorld'],
    'hash' : '',
    'jni_onload_info': {
        'signature' : [],
        'is_cluster_center' : true,
        'distance_from_center' : 0.0,
        'variations': ['monodroid2']
    }
});

db.clusters.insert({
    'so_file_name' : 'monodroid2', 
    'apks_found_in' : ['XamarinHelloWorld'],
    'hash' : '',
    'jni_onload_info': {
        'signature' : [],
        'is_cluster_center' : false,
        'distance_from_center' : 0.1,
        'variations': []
    }
});

