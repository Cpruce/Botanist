// Userlist data array for filling in info box
var userListData = [];




// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    //populateTable();

	// Username link click
    //$('#userList table tbody').on('click', 'td a.linkshowuser', showUserInfo);

	// Add Wesource button click
	$('#btnWsAdd').on('click', addWesource);
		

	// Delete User link click
	//$('#userList table tbody').on('click', 'td a.linkdeleteuser', deleteUser);


    var ext = window.location.href.split("/").pop();
    if(ext == 'rnr' || ext == 'parking' || ext == 'other' || ext == 'appliances'){
        populateTable(ext);    
    }

});


// Functions =============================================================
function giveBack(event){
	var wesourceName = $(event.target).parent().siblings('h2').text();

	// increment availability thru ajax
	$.ajax({
			type:'POST',
			url: '/wesources/giveBack/' + wesourceName,
			success:function(data){
				console.log("success");
				console.log(data);
				if(!(JSON.stringify(data)).contains('error')){
                    console.log(data);

                    $(event.target).parent().siblings('h4').value = 'Availability: ' + data; 
                }                


			},
			error: function(data){
				console.log("error");
				console.log(data);
			}
		});
	

};

function takeOut(event){
    var wesourceName = $(event.target).parent().siblings('h2').text();

    // increment availability thru ajax
    $.ajax({
            type:'POST',
            url: '/wesources/takeOut/' + wesourceName,
            success:function(data){
                console.log("success");
                console.log(data);
                if(!(JSON.stringify(data)).contains('error')){
                    console.log(data);

                    $(event.target).parent().siblings('h4').value = 'Availability: ' + data;                
                }                


            },
            error: function(data){
                console.log("error");
                console.log(data);
            }
        });
};


function populateTable(type) {

    var ext = '/' + type + '/' + type + 'list'; 
    var tnContent = '';
    var i = 0;

    $.getJSON( ext, function( data ) {
       // force synchronous action 
    }).done(function(data){
		   //so we can have three cols per row
           var rowIndex = 0; 
                        
           $.each(data, function(){

                if (rowIndex % 3 === 0) tnContent += '<div class="row">';
                        
				tnContent += '<div class="col-md-4"><div class="thumbnail">';
				
				tnContent += '<img src="http://localhost:3000/img/' + this.img + '" style="height: 40vh;" />';
				tnContent += '<div class="caption"><h2>'+this.wesource+'</h2><p><h3>Location: '+this.location+'</h3><h4>Availability: '+this.availability+'</h4><h5>Max:' + this.max + '</h5></p>';
				//tnContent += '<div class="progress progress-striped active"><div class="bar" style="width: 50%;"></div></div>';
				if(this.availability > 0 && this.availability < this.max){
					tnContent += '<p><div class="btn-group btn-group-justified"><a class="btn btn-primary plus" role="button">Finish</a> <a class="btn btn-success minus" role="button">Reserve</a></div></p></div></div></div>';
				}
				else if(this.availability > 0){
					tnContent += '<p><div class="btn-group btn-group-justified"><a class="btn btn-success minus" role="button">Reserve</a></div></p></div></div></div>'; 
				}
				else{
					tnContent += '<p><div class="btn-group btn-group-justified"><a class="btn btn-primary plus" role="button">Finish</a></div></p></div></div></div>';
				}


				if (rowIndex % 3 === 2) tnContent += '</div>';

				rowIndex+=1;	
			
          		$('#' + type + 'list').html(tnContent);
				});
        	$('.btn.minus').click(giveBack);
        	$('.btn.plus').click(takeOut); 
		

	});
};


// Update User
function updateUser(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to update this user?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            type: 'POST',
            url: '/users/updateuser/' + $(this).attr('rel')
        }).done(function( response ) {

            // Check for a successful (blank) response
            if (response.msg === '') {
            }
            else {
                alert('Error: ' + response.msg);
            }

        });

    }
    else {

        // If they said no to the confirm, do nothing
        return false;

    }

};

 
// Delete User
function deleteUser(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this user?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            type: 'DELETE',
            url: '/users/deleteuser/' + $(this).attr('rel')
        }).done(function( response ) {

            // Check for a successful (blank) response
            if (response.msg === '') {
            }
            else {
                alert('Error: ' + response.msg);
            }


        });

    }
    else {

        // If they said no to the confirm, do nothing
        return false;

    }

};

// Add User
function addUser(event) {
    event.preventDefault();

    // Super basic validation - increase errorCount variable if any fields are blank
    var errorCount = 0;
    $('#addUser input').each(function(index, val) {
        if($(this).val() === '') { errorCount++; }
    });

    // Check and make sure errorCount's still at zero
    if(errorCount === 0) {

        // If it is, compile all user info into one object
        var newUser = {
            'surname': $('#addUser fieldset input#usr').val(),
            'email': $('#addUser fieldset input#inputUserEmail').val(),
            'givenName': $('#addUser fieldset input#inputUserGivenname').val(),
            'password': $('#addUser fieldset input#inputUserPassword').val(),
            //'location': $('#addUser fieldset input#inputUserLocation').val(),
            //'gender': $('#addUser fieldset input#inputUserGender').val()
        }

        // Use AJAX to post the object to our adduser service
        $.ajax({
            type: 'POST',
            data: newUser,
            url: '/users/adduser',
            dataType: 'JSON'
        }).done(function( response ) {

            // Check for successful (blank) response
            if (response.msg === '') {

                // Clear the form inputs
                $('#addUser fieldset input').val('');


            }
            else {

                // If something goes wrong, alert the error message that our service returned
                alert('Error: ' + response.msg);

            }
        });
    }
    else {
        // If errorCount is more than 0, error out
        alert('Please fill in all fields');
        return false;
    }
};

// Add Wesource
function addWesource(event) {
    event.preventDefault();
    // Super basic validation - increase errorCount variable if any fields are blank
    var errorCount = 0;
    var id;
    $('#addWs input').each(function(index, val) {
        id = $(this).attr('id');
        
        if((id == 'loc' || id == 'ws' || id == 'img' || id == 'amount' || 
                id == 'type') && $(this).val() === '') { 
            
            errorCount++; 
        }

    });

    // Check and make sure errorCount's still at zero
    if(errorCount === 0) {
        
        
        // If it is, compile all user info into one object
        var newWesource;
        //if($('#addWs input#limit').val() == ''){
            newWesource = new FormData();
            newWesource.append( 'img', $('#addWs input#img').prop('files') );
            newWesource.append('wesource', $('#addWs input#ws').val());
            newWesource.append('location', $('#addWs input#loc').val());
            newWesource.append('availability', $('#addWs input#amount').val());
            newWesource.append('img', $('#addWs input#img').val());
            newWesource.append('type', $('#addWs input#type').val());
            newWesource.append('max', $('#addWs input#amount').val());
            if ($('#addWs input#limit').val())
                newWesource.append('time_limit', $('#addWs input#limit').val());

            // newWesource = {
            //     'wesource': $('#addWs input#ws').val(),
            //     'location': $('#addWs input#loc').val(),
            //     'availability': $('#addWs input#amount').val(),
            //     'img': $('#addWs input#img').val(),
            //     'type': $('#addWs input#type').val(),
            //     'max': $('#addWs input#amount').val()
            // }
        //}
        // else{

        //     newWesource = {
        //         'wesource': $('#addWs input#ws').val(),
        //         'location': $('#addWs input#loc').val(),
        //         'availability': $('#addWs input#amount').val(),
        //         'img': $('#addWs input#img').val(),
        //         'type': $('#addWs input#type').val(),
        //         'max': $('#addWs input#amount').val(),
        //         'time_limit': $('#addWs input#limit').val()
        //     } 

        // }
        
        $.ajax({
                type:'POST',
                url: '/wesources/addwesource',
                data:newWesource,
                processData: false,
                contentType: false,
                success:function(data){
                    console.log("success");
                    console.log(data);
                    if(data.msg == ''){
                        console.log('yay');
                    
                        var name = $('input#img').val();
				        var file = $('input#img').prop('files');	

                        
    
                        /*$.ajax({
                            type:'POST',
                            url: '/wesources/img/' + name,
                            data: new FormData($('form.col-xs-5')),
                            cache:false,
                            contentType: false,
                            processData: false,
                            success:function(data){
                                console.log("success");
                                console.log(data);
                                if(data.msg == ''){
                                    console.log('yay');
                                }                


                            },
                            error: function(data){
                                console.log("error");
                                console.log(data);
                            }
                        });*/
  						    

                    }                


                },
                error: function(data){
                    console.log("error");
                    console.log(data);
                }
            });

        /*$("#ImageBrowse").on("change", function() {
            $("#btnWsAdd").submit();
        });*/
    }
    else {
        // If errorCount is more than 0, error out
        alert('Please fill in all fields');
        return false;
    }
};


// Show User Info
function showUserInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve username from link rel attribute
    var thisUserName = $(this).attr('rel');

    // Get Index of object based on id value
    var arrayPosition = userListData.map(function(arrayItem) { return arrayItem.username; }).indexOf(thisUserName);

	// Get our User Object
    var thisUserObject = userListData[arrayPosition];

    //Populate Info Box
    $('#userInfoName').text(thisUserObject.fullname);
    $('#userInfoAge').text(thisUserObject.age);
    $('#userInfoGender').text(thisUserObject.gender);
    $('#userInfoLocation').text(thisUserObject.location);
};

// Pretty file
if ($('.prettyFile').length) {
    $('.prettyFile').each(function() {
        var pF          = $(this),
            fileInput   = pF.find('input[type="file"]');
 
        fileInput.change(function() {
            // When original file input changes, get its value, show it in the fake input
            var files = fileInput[0].files,
                info  = '';
            if (files.length > 1) {
                // Display number of selected files instead of filenames
                info     = files.length + ' files selected';
            } else {
                // Display filename (without fake path)
                var path = fileInput.val().split('\\');
                info     = path[path.length - 1];
            }
 
            pF.find('.input-append input').val(info);
        });
 
        pF.find('.input-append').click(function(e) {
            e.preventDefault();
            // Make as the real input was clicked
            fileInput.click();
        })
    });
}
