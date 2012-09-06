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


/*
$(document).ready(function() {
    var NewUserForm = $('#NewUserForm');
    NewUserForm.validate();
});
*/


// Take a UserName and UserPass, pack them into
// a JSON and send it to the server/database bia
// an ajax post request.  Get the result and determine
// if the login was successful or not.
// If it was successful, send the user to the home page
// (May want to consider using the "Next" variable in the head)
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
	//window.location.reload()
	window.location.href = "/";
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


// Bind the 'LoginUser' button to an action that
// collects the information from the user form and 
// calls the LoginUser function.
// (Refactor: Take the specific parts of the LoginUser
//  method above (ie the page redirect at the end) and
//  put them into this method.  Keep the above method
//  as a pure javascript function that submits a requiest
//  and returns a flag.  It's... cleaner)
$(document).ready(function() {
    $('#LoginUser').live('click', function() {
	
	console.log("LoginUser - Begin");
	
	// Get the html form by id,
	// serialize it, 
	// and send it to python
	// using jquery/ajax
	var LoginForm = $('#LoginForm');
	
	// Run jquery validation
	if( ! LoginForm.valid() ) {
	    console.log("Error: Login form is invalid.");
	    $("#LoginResult").html("Error: Login form is invalid.").show();
	    return false;
	}

	var UserName = $('#LoginTable #UserName').val();
	var UserPass = $('#LoginTable #password').val();

	LoginUser(UserName, UserPass);
	console.log("LoginUser() - End");

	return false;
    });
});



