


$(document).ready(function() {
    $('#CreateBeef').live('click', function() {
	
	console.log("CreateBeef() - Begin");
	
	// Get the html form by id,
	// serialize it, 
	// and send it to python
	// using jquery/ajax
	var CreateBeefForm = $('#CreateBeefForm');
	var BeefArray = CreateBeefForm.serializeArray();

	// Run jquery validation
	CreateBeefForm.validate();
	if( ! CreateBeefForm.valid() ) {
	    console.log("Error: Form is invalid.");
	    $("#Result").html("Error: Form is invalid.").show();
	    return false;
	}

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
		var message = data["message"];
		console.log( "Message: " + message );
		$("#Result").html(message).show();
	    }
	}
	
	// Submit the AJAX query
	$.post( "/api/create_beef", CreateBeefForm.serialize(), successCallback );
	console.log("CreateBeefFromForm() - Submittted Activity AJAX request");
	console.log("CreateBeef() - End");
	return false;

    });
});
