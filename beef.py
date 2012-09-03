

import json

from flask import jsonify

import pymongo
import bson.objectid

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
        print "_addToDatabase() - Error: Failed to connect to database"
        raise

    # Check if the 'activities' collection exists:
    if not 'beef' in db.collection_names():
        print "_addToDatabase() - ERROR: 'beef' collection doesn't exist"
        raise Exception("Collection 'beef' Doesn't Exist in Database")

    try:
        beef_collection = db[collection_name]
    except:
        print "_addToDatabase() - Failed to connect to %s collection" % collection_name
        raise

    return beef_collection


def _addToDatabase(beef_dict):
    """ Add (or update) a beef to the database
    
    The argument is a dictionary of the beef information

    """

    try:
        beef_collection = _getCollection("beef")
    except:
        print "Failed to get collection in _addToDatabase"
        raise

    '''
    try:
        db = _connectToDatabase()
    except:
        print "_addToDatabase() - Error: Failed to connect to database"
        raise

    # Check if the 'activities' collection exists:
    if not 'beef' in db.collection_names():
        print "_addToDatabase() - ERROR: 'beef' collection doesn't exist"
        raise Exception("Collection 'beef' Doesn't Exist in Database")

    try:
        beef_collection = db['beef']
    except:
        print "_addToDatabase() - Failed to connect to 'beef' collection"
        raise
    '''

    try:
        # Edit the activity's id
        if "_id" in beef_dict:
            print "Saving object with id: %s" % beef_dict["_id"]
            beef_dict["_id"] = bson.objectid.ObjectId(beef_dict["_id"])

        # Create or update the collection
        saved_id = beef_collection.save(beef_dict)
        print "Saved beef with id %s" % saved_id
    except:
        print "_addToDatabase() - Error: Failed to add beef to database"
        raise

    return


class UserClass(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

        def is_active(self):
            return self.active

def _check_db(userid):
    # query database (again), just so we can pass an object to the callback

    try:
        users_collection = _getCollection("users")
    except:
        print "Failed to get collection in _check_db"
        raise

    db_check = users_collection.find_one({ 'userid' : userid })
    UserObject = UserClass(db_check['username'], userid, active=True)

    if UserObject.id == userid:
        return UserObject
    else:
        return None

def _get_user(username):
    # check MongoDB for the existence of the entered username

    try:
        users_collection = _getCollection("users")
    except:
        print "Failed to get collection in _get_user"
        raise

    db_result = users_collection.find_one({ 'username' : username })
    
    result_id = int(db_result['userid'])
    
    # create User object/instance
    User = UserClass(db_result['username'], result_id, active=True)

    return User


def create_beef(request):
    """ Add an activity to the database

    """

    print "add_beef - Begin()"

    if request.method != 'POST':
        print "add_beef - ERROR: Expected POST http request"
        return jsonify(flag="error")

    # Get the serialized activity JSON object
    # from the request
    beef_dict = json.loads( request.form['beef'] )

    if beef_dict == None:
        print "add_beef() - ERROR: Input beef_dict is 'None'"
        return jsonify(flag="error")
    
    # Add it to the database
    try:
        _addToDatabase(beef_dict)
    except:
        print "add_beef() - Caught exception in _addToDatabase"
        return jsonify(flags="error")

    print "add_beef() - Success"
    return jsonify(flag="success")


def latest(num_entries=10):
    """ Return a list of 10 entries

    """

    # Get the database
    try:
        beef_collection = _getCollection("beef")
    except:
        print "Failed to get collection in _addToDatabase"
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
