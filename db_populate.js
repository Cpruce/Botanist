/* Cory Pruce 
 *
 * Script to populate 
 * the database upon
 * initialization
 *
 * */

conn = new Mongo();
db = connect("SignatureDB");

// clear collections if already exist. 
// REMOVE after adding actual data
db.users.remove({});
db.instances.remove({});

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

db.instances.insert({
    'instance_id' : 1,
    'so_file_name' : 'monodroid', 
    'apks_found_in' : ['XamarinHelloWorld'],
    'specific_symbols_list' : [],
    'hash' : '',
    'jni_onload_info': {
        'signature' : '',
        'is_cluster_center' : true,
        'distance_from_center' : 0.0
    }
});

db.instances.insert({
    'instance_id' : 2,
    'so_file_name' : 'monodroid2', 
    'apks_found_in' : ['XamarinHelloWorld'],
    'specific_symbols_list' : [],
    'hash' : '',
    'jni_onload_info': {
        'signature' : '',
        'is_cluster_center' : true,
        'distance_from_center' : 0.0
    }
});

