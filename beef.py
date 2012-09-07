

import json
import datetime
from collections import OrderedDict

from flask import jsonify

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

items = ["BeefTitle", "BeefOpponent", "BeefDescription", "TimeCreated", "_id"]

'''
title_dict = {}
title_dict["CreatedByName"] = "Created By"
title_dict["CreatedById"] = "Created By (id)"
title_dict["TimeCreated"] = "Creation Time"
title_dict["BeefTitle"] = "Title"
title_dict["beef_title"] = "Title" #deprecated
title_dict["BeefOpponent"] = "Beef Against"
title_dict["beef_opponent"] = "Against" #deprecated
title_dict["BeefDescription"] = "Beef Description"
title_dict["comment"] = "Beef Description"
#title_dict["ArgumentLeft"] = "Beef's Argument"
#title_dict["ArgumentRight"] = "Defence's Argument"
title_dict["CommentList"] = "Comments"
'''

def _get_dict_subset(dict, items):
    if items==None: return dict
    beef_dict = OrderedDict()
    for item in items:
        beef_dict[item] = dict[item]
    return beef_dict


def _title_map(name):
    """ A mapping of database column titles to html (pretty) titles

    """

    #if name in title_dict:
    #    return title_dict[name]

    return name

     
def _format_dict(beef_dict, items):
    """ Format the titles of a return dict

    """

    beef_dict = _get_dict_subset(beef_dict, items)
    beef_dict['TimeCreated'] = beef_dict["TimeCreated"].strftime("%A %d. %B %Y")
    '''
    for key in beef_dict:
        if key in title_dict:
            new_key = _title_map(key)
            beef_dict[new_key] = beef_dict.pop(key)
        else:
            pass
    '''        
    return beef_dict


def create_beef(request):
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

    if request.method != 'POST':
        print "add_beef - ERROR: Expected POST http request"
        return jsonify(flag=1)

    # Get the serialized activity JSON object
    # from the request
    if 'beef' not in request.form:
        print "add_beef() - ERROR: 'beef' table not in request"
        return jsonify(flag=1)
        
    form_dict = json.loads( request.form['beef'] )
    if form_dict == None:
        print "add_beef() - ERROR: Input beef_dict is 'None'"
        return jsonify(flag=1)
    print form_dict
    
    # Create the dictionary to be added
    # to the database
    beef_dict = {}
    beef_dict["BeefTitle"] = form_dict["BeefTitle"]
    beef_dict["BeefOpponent"] = form_dict["BeefOpponent"]
    beef_dict["BeefDescription"] = form_dict["BeefDescription"]

    beef_dict["CreatedByName"] =  current_user.name
    beef_dict["CreatedById"] = bson.objectid.ObjectId(current_user.id)
    beef_dict["TimeCreated"] = datetime.datetime.utcnow()
    beef_dict["ArgumentLeft"]  = ""
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
    to_fetch = items + ["ArgumentLeft", "ArgumentRight", "VotesFor", "VotesAgainst"]

    beef_collection = getCollection("beef")
    beef_entry = beef_collection.find_one({"_id" : bson.objectid.ObjectId(_id)})
    
    if beef_entry==None:
        print "get_beef(): Failed to find entry with _id %s:" % _id
        raise InvalidEntry("Beef with Id Not Found")
    else:
        print "Successfully found entry: %s" % _id

    beef_dict = _format_dict(beef_entry, to_fetch)

    # Now, get the parameters for the template generation
    kwargs = {}
    kwargs['argument_left'] = beef_dict.pop("ArgumentLeft")
    kwargs['argument_right'] = beef_dict.pop("ArgumentRight")
    kwargs['VotesFor'] = beef_dict.pop("VotesFor")
    kwargs['VotesAgainst'] = beef_dict.pop("VotesAgainst")


    beef_owner_id = get_beef_owner(_id)
    if current_user.get_id() == beef_owner_id:
        kwargs['beef_owner']=True
    else:
        kwargs['beef_owner']=False

    print beef_dict
    print kwargs
    return (beef_dict, kwargs)


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

