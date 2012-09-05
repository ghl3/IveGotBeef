$(document).ready(function() {
    $('#CreateBeef').live('click', function() {
	
	console.log("CreateBeef() - Begin");
	
	// Get the html form by id,
	// serialize it, 
	// and send it to python
	// using jquery/ajax
	var NewBeefForm = $('#NewBeefForm');
	var BeefArray = NewBeefForm.serializeArray();

	// Create a javascript dict object out
	// of that encoded dict
	var BeefJSON = {};
	for (i in BeefArray) {
	    BeefJSON[BeefArray[i].name] = BeefArray[i].value
	}

	console.log("Create new Beef and submit to DB");
	console.log( JSON.stringify(BeefJSON) );
	BeefJSON = JSON.stringify( BeefJSON );

	// Create a call-back function
	// for debugging and logging
	function successCallback(data) {
	    if( data["flag"]=="0" ) {
		console.log("Successfully Created Beef");

		// We want to move to the newly created entry
		beef_id = data["beef_id"];
		window.location.href = "/Beef?_id=" + beef_id;

	    }
	    else {
		console.log("ERROR: Failed to create beef");
	    }
	}
	
	// Submit the AJAX query
	$.post( "/api/create_beef", {beef : BeefJSON}, successCallback );
	console.log("CreateBeefFromForm() - Submittted Activity AJAX request");
	console.log("CreateBeef() - End");
	return false;

    });
});

function CreateBeefFromForm( form ) {

}


/*
$(document).ready(function() {
    $('#CreateBeef').live('click', function() {
	
	console.log("CreateBeef() - Begin");
	
	// Get the html form by id,
	// serialize it, 
	// and send it to python
	// using jquery/ajax
	var NewBeefForm = $('#NewBeefForm');
	CreateBeefFromForm( NewBeefForm );
	//HideNewBeefForm();

	console.log("CreateBeef() - End");
	return false;
    });
});

function CreateBeefFromForm( form ) {

    console.log("CreateBeefFromFor() - Begin");

    var BeefArray = form.serializeArray();

    // Create a javascript dict object out
    // of that encoded dict
    var BeefJSON = {};
    for (i in BeefArray) {
	BeefJSON[BeefArray[i].name] = BeefArray[i].value
    }

    console.log("Create new Beef and submit to DB");
    console.log( JSON.stringify(BeefJSON) );
    BeefJSON = JSON.stringify( BeefJSON );

    // Create a call-back function
    // for debugging and logging
    function successCallback(data) {
	if( data["flag"]=="success" ) {
	    console.log("Successfully added Activity");

	    // We want to move to the newly created entry
	    beef_id = data["beef_id"];
	    window.location.href = "/Beef?_id=" + beef_id;

	}
	else {
	    console.log("ERROR: Failed to add Activity");
	}
    }
    
    // Submit the AJAX query
    $.post( "/api/create_beef", {beef : BeefJSON}, successCallback );
    console.log("CreateBeefFromForm() - Submittted Activity AJAX request");

    return false;

}
*/


/*
$(document).ready(function() {
    $('.GetBeefButton').live('click', function() {
	
	console.log("GetBeefButton() - Begin");
	console.log( this.getAttribute("id") );

	// Get the html form by id,
	// serialize it, 
	// and send it to python
	// using jquery/ajax
	var NewBeefForm = $('#NewBeefForm');
	CreateBeefFromForm( NewBeefForm );
	//HideNewBeefForm();

	console.log("CreateBeef() - End");
	return false;
    });
});
*/



$(document).ready(function() {
    $('#CreateUser').live('click', function() {
	
	console.log("CreateUser - Begin");
	
	// Get the html form by id,
	// serialize it, 
	// and send it to python
	// using jquery/ajax
	var UserTable = $('#CreateUserTable');
	
	var UserName = $('#CreateUserTable #UserName').val();
	var UserPass = $('#CreateUserTable #UserPass').val();

	function successfulCallback(data) {

	    if( data["flag"]!=0 ) {
		console.log("Error: failed to add User");
		return;
	    }

	    if( data["UserAdded"]!=0) {
		console.log("Error: Failed to add user");
		console.log(data["Message"]);
		return;
	    }

	    console.log("Successfully Added User");
	    console.log("Logging in user:");
	    LoginUser(UserName, UserPass);

	    return;
	}

	$.post("/api/add_user", {username: UserName, password: UserPass}, successfulCallback );

	console.log("CreateUser() - End");
	return false;
    });
});


function LoginUser(UserName, UserPass) {

    // Create the callback
    function successfulCallback(data) {

	if( data["flag"]!=0 ) {
	    console.log("Error: failed to login User");
	    return;
	}

	if( data["UserLoggedIn"]!=0) {
	    console.log("Error: Failed to login user");
	    console.log(data["Message"]);
	    $("#LoginResult").html("Login failed.  Invalid Username Password Combination").show();
	    return;
	}

	console.log("Successfully Logged In User");
	$("#Login").hide();
	$("#LoginResult").html("Successfully logged in.  Welcome, " + UserName + ".").show();
	// window.location.href = '/';
	return;
    }

    function errorCallback(data) {
	
	$("#LoginResult").html("An Error Occurred.  Please Try again.").show();

    }

    // Loging using ajax
    $.post("/api/login", {username: UserName, password: UserPass}, successfulCallback )
	.error(errorCallback);

}

$(document).ready(function() {
    $('#LoginUser').live('click', function() {
	
	console.log("LoginUser - Begin");
	
	// Get the html form by id,
	// serialize it, 
	// and send it to python
	// using jquery/ajax
	var UserTable = $('#LoginUserTable');
	
	var UserName = $('#LoginUserTable #UserName').val();
	var UserPass = $('#LoginUserTable #UserPass').val();

	LoginUser(UserName, UserPass);
	console.log("LoginUser() - End");

	return false;
    });
});



