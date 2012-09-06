


// Handle the various functions necessary
// for displaying and editing beef voting, 
// editing, commenting, etc, etc and so forth



// Increment the votes
$(document).ready(function() {
    $('#VoteLeft').live('click', vote_for );
    $('#VoteRight').live('click', vote_against );
});

function vote_for() { vote("for");}
function vote_against() { vote("for");}

function vote(vote_for) {
    // Idea: At template rendering stage,
    // determine whether the user has voted
    // for this beef or not (if he's not
    // the user of course).  Could save
    // a database query later.

    // This is voting in favor of the beef
    // ie, on the side of the guy with beef

    // Hide the result div (duh)
    $("#Result").html("").hide();

    // Get the beef id
    var beef_id = getURLParameter("_id");
    if( beef_id == null ) {
	console.log("A weird error occured, certainly there should be an id in the url");
	return false;
    }

    function successfulCallback(data) {

	if( data["flag"]!=0 ) {
	    console.log("Error: Failed to cast vote");
	    return false;
	}

	if( data["action"]=="nothing" ) {
	    console.log("Result: Do nothing.");
	    return false;
	}
	else if( data["action"]=="increment_for" ) {
	    console.log("Incrementing the vote 'for'.");
	    $("#VotesFor").val() += 1;
	    return false;
	}
	else if( data["action"]=="increment_against" ) {
	    console.log("Incrementing the vote 'against'.");
	    $("#VotesAgainst").val() += 1;
	    return false;
	}
	else if( data["action"]=="swap_to_for" ) {
	    console.log("Swapping vote to 'for'.");
	    $("#VotesFor").val() += 1;
	    $("#VotesAgainst").val() -= 1;
	    return false;
	}
	else if( data["action"]=="swap_to_against" ) {
	    console.log("Swapping vote to 'against'.");
	    $("#VotesAgainst").val() += 1;
	    $("#VotesFor").val() -= 1;
	    return false;
	}
	else {
	    console.log("Error: An unknown control flow occured");
	    return false;
	}
	
    } // End Callback

    function errorCallback(data) {
	console.log("Error callback: Database query failed");
	$("#Result").html("Database error: Vote not cast. Please try again").show();
    }

    // Send the vote to the server/database
    // and make them do most of the work
    $.post("/api/vote_for", {"beef_id" : beef_id, "vote_for" : vote_for}, successfulCallback)
	.error(errorCallback);
}

