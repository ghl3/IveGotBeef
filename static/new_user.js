

// Get a new user form, validate the input, send the 
// form to the server/database via ajax post, 
// retrieve the reuslt and determine if it was successful,
// and print a message in the result div (stay on page)
$(document).ready(function() {
    $('#CreateUser').live('click', function() {
	
	console.log("CreateUser - Begin");

	$("#Result").html("").hide();

	// Get the html form by id,
	// serialize it, 
	// and send it to python
	// using jquery/ajax
	var UserTable = $('#CreateUserTable');
	
	var UserName = $('#CreateUserTable #username').val();
	var UserPass = $('#CreateUserTable #password').val();

	var NewUserForm = $('#NewUserForm');

	// Run jquery validation
	NewUserForm.validate();
	if( ! NewUserForm.valid() ) {
	    console.log("Error: Form is invalid.");
	    $("#Result").html("Error: Form is invalid.").show();
	    return false;
	}

	var UserArray = NewUserForm.serializeArray();
	var UserJSON = {};
	for (i in UserArray) {
	    UserJSON[UserArray[i].name] = UserArray[i].value
	}
	//UserJSON=JSON.stringify(UserJSON);
	console.log(UserJSON);

	if( UserJSON["password"]=="" || UserJSON["confirm"]=="" ){
	    console.log("Error: You must enter your password, and again for confirmation");
	    $("#Result").html("Error: You must enter your password, and again for confirmation").show();
	    return false;
	} 
	if( UserJSON["password"] != UserJSON["confirm"] ){
	    console.log("Error: Passwords don't match");
	    $("#Result").html("Error: Your passwords don't match").show();
	    return false;
	} 

	// Don't forget to get rid of 
	// password2 once we validate it
	// delete UserJSON["password2"];

	// Figure out where to send the user
	var next = getURLParameter("next");

	function successfulCallback(data) {

	    if( data["flag"]!=0 ) {
		console.log("Error: failed to add new User");
		return false;
	    }

	    if( data["UserAdded"]!=0) {
		console.log("Error: Failed to add new user");
		console.log(data["Message"]);
		return false;
	    }

	    console.log("Successfully Added New User");
	    console.log("Logging in user:");
	    LoginUser(UserName, UserPass, next);

	    return false;
	}

	//$.post("/api/add_user", {user: JSON.stringify(UserJSON)}, successfulCallback );
	$.post("/api/new_user", NewUserForm.serialize(), successfulCallback );

	console.log("CreateUser() - End");
	return false;
    });
});
