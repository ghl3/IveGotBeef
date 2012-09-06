
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

	var next = getURLParameter("next");

	LoginUser(UserName, UserPass, next);
	console.log("LoginUser() - End");

	return false;
    });
});



