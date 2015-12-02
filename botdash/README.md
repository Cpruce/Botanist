## How to Use
1. git clone https://github.com/Cpruce/OpenDER.git && cd OpenDER/bootstrap_dashboard
2. Install dependencies: npm install
3. Build: gulp build
4. Lauch: gulp run

## Public RESTful APIs
### /api/registerhh  
Type: POST  
Parameters: None  
Function: Register a new homehub, and return its uid

### /api/listhhs
Type: GET  
Parameters: None  
Function: Get all homehubs

### /api/hhinfo
Type: GET  
Parameters: ?uid="homehub uid"  
Function: Get the detailed homehub information

### /api/hhinfo  
Type: POST  
Parameters: {"uid" : "the homehub uid", "info" : "JSON String of the fileds to be updated, such as price or device list"}  
Function: Update the specific homehub information

### /api/hhstatus
Type: POST  
Parameters: {"uid" : "the homehub uid", "power" : "power consumption", [device status list]}  
Function: Send current homehub status to the cloud control

### /api/price
Type: GET  
Parameters: ?uid="homehub uid"  
Function: Get current homehub power price

### /api/price
Type: POST  
Parameters: {"uid" : "the homehub uid", "price" : current price}   
Function: Set the homehub price

## MongoDB Collections
1. homehubs - Store the basic information of a homehub, including uuid, name, longitude, latitude and device list, current power price
2. hhstatus - Store the homehub status, including uuid, list of device status (power usage, on/off), reporting timestamp


## TODOs
1. Add APIs for internal usage. (Rendering data on dashboard)
2. Perfomance evaluation
3. Security assessment
