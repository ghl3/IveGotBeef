


// Handle the various functions necessary
// for displaying and editing beef voting, 
// editing, commenting, etc, etc and so forth



// Increment the votes
$(document).ready(function() {
    $('#VoteLeft').live('click', vote_for );
    $('#VoteRight').live('click', vote_against );
});

function vote_for() { vote("for"); }
function vote_against() { vote("against"); }

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

	var VotesFor     = parseFloat( $("#VotesTotalLeft").html() );
	var VotesAgainst = parseFloat( $("#VotesTotalRight").html() );

	console.log("Initial votes for: " + VotesFor);
	console.log("Initial votes against: " + VotesAgainst);

	if( data["action"]=="nothing" ) {
	    console.log("Result: Do nothing.");
	    return false;
	}
	else if( data["action"]=="increment_for" ) {
	    console.log("Incrementing the vote 'for'.");
	    $("#VotesTotalLeft").html(VotesFor + 1);
	    return false;
	}
	else if( data["action"]=="increment_against" ) {
	    console.log("Incrementing the vote 'against'.");
	    $("#VotesTotalRight").html(VotesAgainst + 1);
	    return false;
	}
	else if( data["action"]=="swap_to_for" ) {
	    console.log("Swapping vote to 'for'.");
	    $("#VotesTotalLeft").html(VotesFor + 1);
	    $("#VotesTotalRight").html(VotesAgainst - 1);
	    return;
	}
	else if( data["action"]=="swap_to_against" ) {
	    console.log("Swapping vote to 'against'.");
	    $("#VotesTotalRight").html(VotesAgainst + 1);
	    $("#VotesTotalLeft").html(VotesFor - 1);
	    return;
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

//
// Comments
//


// Increment the votes
$(document).ready(function() {
    $('#NewCommentWrapper').hide();
    $('#AddComment').live('click', AddComment );
    $('#SaveComment').live('click', SaveComment );
    $('#CancelComment').live('click', CancelComment );
});



function AddComment() {

    // Create the text field for adding a
    // new comment.  This does not yet save
    // the comment.

    $('#NewCommentWrapper').show();
    $('#AddComment').hide();
    $('#NoCommentsYet').hide();
    

    //$("#NewCommentWrapper").scrollTop($("#NewCommentWrapper")[0].scrollHeight);
    //$('#NewCommentWrapper').animate({scrollTop: $("#NewCommentWrapper").offset().top}, 'slow');

    $('html, body').animate({scrollTop: $(document).height()-$(window).height()},
			    'fast',"linear");
}

function CancelComment() {

    // Cancel the comment, and restore
    // things as they were before

    $('#NewCommentWrapper').hide();
    $('#AddComment').show();
    $('#NoCommentsYet').show();
    


}


function SaveComment() {

    // Take the content in the 'AddComment' field, 
    // send it to the db to be save, and if this
    // is successful, show the comment in html

    // Create our callbacks (both good and evil)
    function successfulCallback(data) {

	if( data["flag"]!=0 ) {
	    console.log("Error: Failed to add comment :(");
	    return false;
	}

	// Clear the editable comment
	$("#NewComment").val('');
	$("#Comment_List").append(comment);

	var comment = document.createElement("textarea");
	comment.setAttribute("class", "Comment");
	comment.setAttribute("readonly", "true");
	comment.value = comment_text;

	$("#Comment_List").append(comment);
	$('html').animate( {scrollTop: $("#Comment_List")}, 'slow');
	$('#NewCommentWrapper').hide();
	$('#AddComment').show();
	$('#NoCommentsYet').remove();
    }

    function errorCallback(data) {

	console.log("There was a server error.  Comment not added");

    }

    // Get the information we need and send it to the
    // db via async ajax
    var comment_text = $("#NewComment").val();
    var beef_id = getURLParameter("_id");
    console.log("Comment for beef: " + beef_id + ": " + comment_text);

    $.post("/api/add_comment", {"beef_id" : beef_id, "comment" : comment_text}, successfulCallback)
	.error(errorCallback);

    console.log("Request to add comment made.  Waiting...");

}
