

$(document).ready(function() {
    $('#CreateBeef').live('click', function() {
	
	console.log("CreateBeef() - Begin");
	
	// Get the html form by id,
	// serialize it, 
	// and send it to python
	// using jquery/ajax
	var NewBeefForm = $('#NewBeefForm');
	CreateBeefFromForm( NewBeefForm );
	HideNewBeefForm();

	console.log("CreateBeef() - End");
	return false;
    });
});

function AddBeefFromForm( form ) {

    console.log("AddBeefFromFor() - Begin");

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
	    ClearActivityTable();
	    RefreshActivityList();
	}
	else {
	    console.log("ERROR: Failed to add Activity");
	}
    }
    
    // Submit the AJAX query
    $.post( "/create_beef", {beef : BeefJSON}, successCallback );
    console.log("CreateBeefFromForm() - Submittted Activity AJAX request");

    return false;

}
