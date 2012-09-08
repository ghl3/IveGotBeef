
import json
import datetime
from collections import OrderedDict

from flask import jsonify
from flask import render_template

import pymongo
import bson.objectid

from flask.ext.login import current_user

from common import *

# import flask_login

#
# The tools used by the app
# to connect to, update, and
# display the beef.
#

#items = ["BeefTitle", "BeefOpponent", "BeefDescription", "TimeCreated", "_id"]


# WTF Form
from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators

class BeefForm(Form):
    Title = TextField('Title', [validators.Required(), validators.Length(min=3, max=25)])
    Opponent = TextField('Against', [validators.Required(), validators.Length(min=3, max=25)])
    Description = TextAreaField('Desription', [validators.Required(), validators.Length(min=5, max=1000)])
    Argument = TextAreaField('Argument', [validators.Required(), validators.Length(min=5, max=5000)])


def _get_dict_subset(dict, items):
    if items==None: return dict
    beef_dict = OrderedDict()
    for item in items:
        beef_dict[item] = dict[item]
    return beef_dict


def _format_dict(beef_dict, items=None):
    """ Format the titles of a return dict

    Reduce the elements in a dict to only the
    items we need, and format them for output

    """

    beef_dict = _get_dict_subset(beef_dict, items)
    beef_dict['TimeCreated'] = beef_dict["TimeCreated"].strftime("%a, %B %d, %Y")
    return beef_dict


def get_userId(username):
    """ Given a username, get the user id

    """
    users_collection = getCollection("users")
    user_entry = users_collection.find_one({"username" : username })
    if user_entry==None:
        return None
    else:
        return user_entry["_id"]

def create_beef(beef_form):
    """ Add an activity to the database

    Each Beef in the database has the following entries:
    
    -> CreatedByName - The Name of the createer
    -> CreatedById - The Id of the createer
    -> TimeCreated - The datetime when the beef was created
    -> BeefTitle - The name of this Beef
    -> BeefOpponent - The name of the person this beef is with
    -> BeefDescription - The general description of the beef (w/o main arguments)
    -> ArgumentLeft - The argument by the person with beef
    -> ArgumentRight - The argument (defense) by the person who the beef is with
    -> CommentList - The list of comments from the neutral observers
    """

    print "add_beef - Begin()"

    # Get the serialized activity JSON object
    # from the request
    form_dict = beef_form.data
    print form_dict

    # Make sure that the beef is against a valid opponent
    beef_opponent_id = get_userId(form_dict["Opponent"])
    if beef_opponent_id==None:
        print "Error: Cannot create beef, invalid opponent name: ", form_dict["Opponent"]
        return jasonify(flag=1, message="Invalid Opponent")

    # Create the dictionary to be added
    # to the database
    beef_dict = {}
    beef_dict["BeefTitle"] = form_dict["Title"]
    beef_dict["BeefOpponent"] = form_dict["Opponent"]
    beef_dict["BeefDescription"] = form_dict["Description"]
    beef_dict["BeefOpponentId"] = beef_opponent_id

    beef_dict["CreatedByName"] = current_user.name
    beef_dict["CreatedById"] = bson.objectid.ObjectId(current_user.id)
    beef_dict["TimeCreated"] = datetime.datetime.utcnow()
    beef_dict["ArgumentLeft"]  = form_dict["Argument"]
    beef_dict["ArgumentRight"] = ""
    beef_dict["CommentList"] = []
    beef_dict["VotesFor"] = 0
    beef_dict["VotersFor"] = []
    beef_dict["VotesAgainst"] = 0
    beef_dict["VotersAgainst"] = []

    # Add it to the database
    try:
       beef_id = addToBeefDatabase(beef_dict, "beef")
    except:
        print "add_beef() - Caught exception in _addToBeefDatabase"
        raise

    # Add this beef to the list
    # of the current user's beef
    current_user_id = bson.objectid.ObjectId(current_user.id)

    users_collection = getCollection("users")
    user_in_db = users_collection.find_one({"_id": current_user_id})
    if "beef" not in user_in_db:
        print "Error: Cannot find list of beef in user entry"
        raise InvalidUser("Invalid User Entry in DB")

    user_in_db["beef"].append(beef_id)
    users_collection.save(user_in_db)

    print "add_beef() - Success"
    return jsonify(flag=0, beef_id=beef_id.__str__())


def latest(num_entries=10):
    """ Return a list of 10 entries

    """

    items = ["BeefTitle", "BeefOpponent", "BeefDescription", "TimeCreated", "_id"]
    beef_collection = getCollection("beef")
    beef_list = beef_collection.find(limit=num_entries)
    
    return_list = []
    for entry in beef_list:
        return_list.append(_format_dict(entry, items))

    return return_list


def get_beef(_id):
    """ Get the sigle beef entry with the supplied id

    Return the beef as as dict, and return also a 
    dict representing the keyword arguments for the
    template generation:

    return (beef, kw_args)
    """

    # Be sure to fetch these parameters:
    to_fetch = ["_id", "BeefTitle", "CreatedById", "BeefOpponent", "BeefDescription", 
                "TimeCreated", "ArgumentLeft", "ArgumentRight", 
                "VotesFor", "VotesAgainst", "CommentList"]

    beef_collection = getCollection("beef")
    beef_entry = beef_collection.find_one({"_id" : bson.objectid.ObjectId(_id)})
    
    if beef_entry==None:
        print "get_beef(): Failed to find entry with _id %s:" % _id
        raise InvalidBeef("Beef with Id Not Found")
    else:
        print "Successfully found entry: %s" % _id

    beef_dict = _format_dict(beef_entry, to_fetch)

    # Now, get the parameters for the template generation
    kwargs = {}
    kwargs['argument_left'] = beef_dict.pop("ArgumentLeft")
    kwargs['argument_right'] = beef_dict.pop("ArgumentRight")
    kwargs['VotesFor'] = beef_dict.pop("VotesFor")
    kwargs['VotesAgainst'] = beef_dict.pop("VotesAgainst")

    # Determie who started the beef
    if current_user.get_id() == beef_dict["CreatedById"].__str__():
        kwargs['beef_owner']=True
    else:
        kwargs['beef_owner']=False

    # Determie who the beef is against
    if current_user.get_id() == beef_dict["BeefOpponent"].__str__():
        kwargs['beef_against']=True
    else:
        kwargs['beef_against']=False

    # Now, fetch the comments
    # Comments are stored as ObjectId's
    comments_collection = getCollection("comments")
    comments = beef_dict.pop("CommentList")
    comment_list = []
    for comment_id in comments:
        comment = comments_collection.find_one({"_id" : comment_id})
        comment = _format_dict(comment, ["username", "user_id",  "TimeCreated", "comment"])
        comment_list.append(comment)

    print beef_dict
    print comment_list
    print kwargs
    return (beef_dict, comment_list, kwargs)


def get_beef_owner(_id):
    """ Return the id of the creater of this beef

    """
    beef_collection = getCollection("beef")
    beef_entry = beef_collection.find_one({"_id" : bson.objectid.ObjectId(_id)})
    return beef_entry["CreatedById"].__str__()


def get_beef_list(user_id):
    """ Get the list of beef created by the user with user_id

    """

    user_collection = getCollection("users")
    
    print "Getting beef for user: ", user_id
    user_entry = user_collection.find_one({"_id" : bson.objectid.ObjectId(user_id)})
    beef_id_list = user_entry["beef"]
    print "Beef for user: %s:" % user_id
    print beef_id_list

    beef_collection = getCollection("beef")

    beef_list = []
    for object_id in beef_id_list:
        beef_entry = beef_collection.find_one({"_id" : object_id})
        beef_entry = _format_dict(beef_entry, items)
        beef_list.append(beef_entry)

    print "Beef List: ", beef_list
    return beef_list


def vote(beef_id, user_id, vote_for):
    """ Have a user vote on a particular beef

    vote_for: a 'boolean' parameter to determine
    if we are voting for or against this beef

    This will return a JSON response with two keys: 
       - flag
       - action
     
     The possible results for the "action" response are :
       - increment_for
       - increment_against
       - swap_to_for
       - swap_to_against
       - nothing
     
    """
    
    if vote_for != "for" and vote_for != "against":
        print "Invalid Vote: neither 'for' nor against"
        raise InvalidVote("Must be 'for' or 'against'")


    beef_id_obj = bson.objectid.ObjectId(beef_id)
    user_id_obj = bson.objectid.ObjectId(user_id)

    # Create the return key
    action=None
    
    # First, check that the user hasn't already 
    # voted for this
    user_collection = getCollection("users")
    user_entry = user_collection.find_one({"_id": user_id_obj})
    
    if user_entry==None:
        print "Error: User not found: ", user_id
        return jsonify(flag=1)

    if beef_id in user_entry["votes"]:
        
        previous_vote = user_entry["votes"][beef_id]
        if previous_vote != "for" and previous_vote != "against":
            raise InvalidVote
        elif previous_vote=="for" and vote_for=="for":
            action="nothing"
        elif previous_vote=="against" and vote_for=="against":
            action="nothing"
        elif previous_vote=="for" and vote_for=="against":
            action="swap_to_against"
        elif previous_vote=="against" and vote_for=="for":
            action="swap_to_for"
        else:
            print "Current Vote: ", vote_for, " Previous Vote: ", previous_vote
            raise InvalidVote

    else:
        if vote_for=="for":
            action="increment_for"
        elif vote_for=="aginst":
            action="increment_against"
        else:
            print "Current Vote: ", vote_for
            raise InvalidVote
        pass

    
    # If we don't need to do anything, return right away
    if action=="nothing":
        print "vote_for:", vote_for
        print "Completing Action: ", action
        return jsonify(flag=0, action=action)

    beef_collection = getCollection("beef")
    beef_entry = beef_collection.find_one({"_id" : beef_id_obj})

    if beef_entry==None:
        print "Error: Beef not found: ", beef_id
        return jsonify(flag=1)

    elif action=="increment_for":
        beef_entry["VotesFor"] += 1
        beef_entry["VotersFor"].append(user_id)
        user_entry["votes"][beef_id] = "for"
  
    elif action=="increment_against":
        beef_entry["VotesAgainst"] += 1
        beef_entry["VotersAgainst"].append(user_id)
        user_entry["votes"][beef_id] = "against"

    elif action=="swap_to_for":
        beef_entry["VotesAgainst"] -= 1
        beef_entry["VotesFor"] += 1
        beef_entry["VotersAgainst"] = [voter for voter in beef_entry["VotersAgainst"] if voter != user_id ]
        beef_entry["VotersFor"].append(user_id)
        user_entry["votes"][beef_id] = "for"

    elif action=="swap_to_against":
        beef_entry["VotesFor"] -= 1
        beef_entry["VotesAgainst"] += 1
        beef_entry["VotersFor"] = [voter for voter in beef_entry["VotersFor"] if voter!=user_id ]
        beef_entry["VotersAgainst"].append(user_id)
        user_entry["votes"][beef_id] = "against"

    else:
        print "Undefined behavior"
        raise Exception("Undefined behavior in voting")

    # Save into the database:
    beef_collection.save(beef_entry)
    user_collection.save(user_entry)

    print "Action Completed: ", action
    return jsonify(flag=0, action=action)



def add_comment(user_id, beef_id, comment):
    """ Add a comment to the db and return a response

    The comment is added with the user_id of the
    person who wrote it, the beef_id that it was
    written on, and the string of the comment itself
    
    We of course have to add this comment's id to the
    list of comments in the beef

    We also need to add this comment's id to a 
    user's list of comments

    """

    user_name = current_user.name 
    current_datetime = datetime.datetime.utcnow()
    time_string = current_datetime.strftime("%a, %B %d, %Y")

    comment_dict = {}
    comment_dict["user_id"] = bson.objectid.ObjectId(user_id)
    comment_dict["username"] = user_name #current_user.name #bson.objectid.ObjectId(user_id)
    comment_dict["beef_id"] = bson.objectid.ObjectId(beef_id)
    comment_dict["comment"] = comment
    comment_dict["TimeCreated"] = current_datetime #datetime.datetime.utcnow()

    # First, add the comment to the comment collection
    comments_collection = getCollection("comments")
    comment_id = comments_collection.save(comment_dict)

    # Then, add it to the beef
    beef_collection = getCollection("beef")    
    current_beef = beef_collection.find_one({"_id" : bson.objectid.ObjectId(beef_id)})
    if current_beef == None:
        print "Error: Cannot find beef in collection with id: ", beef_id
        raise InvalidBeef
    current_beef["CommentList"].append(comment_id)
    beef_collection.save(current_beef)

    # And finally, add it to the user
    users_collection = getCollection("users")    
    user_item = users_collection.find_one({"_id" : bson.objectid.ObjectId(user_id)})
    if user_item == None:
        print "Error: Cannot find user in collection with id: ", user_id
        raise InvalidUser
    user_item["comments"].append(comment_id)
    users_collection.save(user_item)
    
    # Okay, we're done.  Boom Sauce
    comment_div = render_template("comment.html", comment=_format_dict(comment_dict))
    return jsonify(flag=0, comment_div=comment_div )


def update_argument(beef_id, argument, position):
    """ Update a beef's argument in the database

    """

    print "Updating Beef argument"

    # Get the user who is attempting to do the update
    user_id = current_user.get_id()

    beef_collection = getCollection("beef")
    beef_entry = beef_collection.find_one({"_id": bson.objectid.ObjectId(beef_id)});
    
    # Check that the right user is trying to do the update
    if not (position == "Left" or position == "Right"):
        print "Invalid 'position' supplied: ", position
        print "Must be 'Left' or 'Right'"
        return jsonify(flag=1)
    elif position=="Left" and user_id != beef_entry["CreatedById"].__str__():
        print "Error: Only the Beef Creator can update the left argument"
        print "Current User: ", user_id, " Beef Creator: ", beef_entry
        return jsonify(flag=1)
    elif position=="Right" and user_id != beef_entry["BeefOpponentId"].__str__():
        print "Error: Only the Beef Against-ee can update the right argument"
        return jsonify(flag=1)
    else:
        pass

    if position=="Left":
        beef_entry["ArgumentLeft"] = argument

    if position=="Right":
        beef_entry["ArgumentRight"] = argument

    beef_collection.save(beef_entry)
    return jsonify(flag=0)
