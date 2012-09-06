

// Get the url parameters (the GET parameters)
// (For some reason, javascript or jquery don't
// do this natively.  Seems odd to me...?
function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}


// Take a UserName and UserPass, pack them into
// a JSON and send it to the server/database bia
// an ajax post request.  Get the result and determine
// if the login was successful or not.
// If it was successful, send the user to the home page
// (May want to consider using the "Next" variable in the head)
function LoginUser(UserName, UserPass, next) {


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
	if( next != null ) window.location.href = next;
	else window.location.href = "/";
	return;
    }

    function errorCallback(data) {
	$("#LoginResult").html("An Error Occurred.  Please Try again.").show();
    }

    // Loging using ajax
    $.post("/api/login", {username: UserName, password: UserPass}, successfulCallback )
	.error(errorCallback);

}
