
import traceback

import json

from flask import jsonify

import pymongo
import bson.objectid

from flask.ext.login import current_user

#import flask_login

#
# The tools used by the app
# to connect to, update, and
# display the beef.
#

def _connectToDatabase():
    """ Get a handle on the mongo db object

    """
    try:
        connection = pymongo.Connection()
    except:
        print "connectToDatabase() - Failed to open connect to MongoDB"
        raise

    try:
        db = connection['i_got_beef']
    except:
        print "connectToDatabase() - Failed to connect to summer_of_george db"
        raise

    return db


def _getCollection(collection_name):
    """ Get a collection from the database

    """
    try:
        db = _connectToDatabase()
    except:
        print "_getCollection() - Error: Failed to connect to database"
        raise

    # Check if the 'activities' collection exists:
    if not 'beef' in db.collection_names():
        print "_getCollection() - ERROR: 'beef' collection doesn't exist"
        raise Exception("Collection " + collection_name + " Doesn't Exist in Database")

    try:
        beef_collection = db[collection_name]
    except:
        print "_getCollection() - Failed to connect to %s collection" % collection_name
        raise

    return beef_collection


def _addToBeefDatabase(beef_dict):
    """ Add (or update) a beef to the database
    
    The argument is a dictionary of the beef information

    """

    try:
        beef_collection = _getCollection("beef")
    except:
        print "Failed to get collection in _addToBeefDatabase"
        raise

    try:
        if "_id" in beef_dict:
            print "Saving object with id: %s" % beef_dict["_id"]
            beef_dict["_id"] = bson.objectid.ObjectId(beef_dict["_id"])

        # Create or update the collection
        saved_id = beef_collection.save(beef_dict)
        print "Saved beef with id %s" % saved_id
    except:
        print "_addToBeefDatabase() - Error: Failed to add beef to database"
        raise

    return saved_id



def create_beef(request):
    """ Add an activity to the database

    """

    print "add_beef - Begin()"

    if request.method != 'POST':
        print "add_beef - ERROR: Expected POST http request"
        return jsonify(flag=1)

    # Get the serialized activity JSON object
    # from the request
    beef_dict = json.loads( request.form['beef'] )

    beef_dict["CreatedByName"] =  current_user.name
    beef_dict["CreatedById"] =  bson.objectid.ObjectId(current_user.id)

    if beef_dict == None:
        print "add_beef() - ERROR: Input beef_dict is 'None'"
        return jsonify(flag=1)
    
    # Add it to the database
    try:
       beef_id = _addToBeefDatabase(beef_dict)
    except:
        print "add_beef() - Caught exception in _addToBeefDatabase"
        print traceback.format_exc()
        return jsonify(flag=1)

    # Add this beef to the list
    # of the current user's beef
    
    current_user_id = bson.objectid.ObjectId(current_user.id)

    try:
        users_collection = _getCollection("users")
    except:
        print "Failed to get collection in create_beef()"
        raise

    user_in_db = users_collection.find_one({"_id": current_user_id})
    if "beef" not in user_in_db:
        print "Error: Cannot find list of beef in user entry"
        raise Exception("Invalid User Entry in DB")

    user_in_db["beef"].append(beef_id)
    users_collection.save(user_in_db)

    print "add_beef() - Success"
    return jsonify(flag=0, beef_id=beef_id)


def latest(num_entries=10):
    """ Return a list of 10 entries

    """

    # Get the database
    try:
        beef_collection = _getCollection("beef")
    except:
        print "Failed to get collection in _latest"
        raise

    return list(beef_collection.find(limit=num_entries))

def get_beef(_id):
    """ Return a list of 10 entries

    """

    # Get the database
    try:
        beef_collection = _getCollection("beef")
    except:
        print "Failed to get collection in _addToDatabase"
        raise
    
    beef_entry = beef_collection.find_one({"_id" : bson.objectid.ObjectId(_id)})
    
    if beef_entry==None:
        print "get_beef(): Failed to find entry with _id %s:" % _id
        raise Exception("Id Not Found")
    else:
        print "Successfully found entry: %s" % _id

    return beef_entry
