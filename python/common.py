
import os
import pymongo
import bson.objectid
from urlparse import urlsplit
from pymongo import Connection
from pymongo.collection import Collection

from collections import OrderedDict

#
# Common database tools for the app
#

class CollectionNotFound(Exception):
    pass

class InvalidUser(Exception):
    pass

class InvalidBeef(Exception):
    pass

class InvalidVote(Exception):
    pass

class InvalidComment(Exception):
    pass

# Check the local url
#url = os.getenv('MONGOLAB_URI', None'mongodb://localhost:27017/ive_got_beef')
url = os.getenv('MONGOLAB_URI', None)
if url==None:
    print "Using Local pymongo"
else:
    parsed = urlsplit(url)
    db_name = parsed.path[1:]
    if '@' in url:
        user_pass = parsed.netloc.split('@')[0].split(':')

def connectToDatabase():
    """ Get a handle on the mongo db object

    """

    if connectToDatabase.LOCAL:

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

    else:
     
        '''
        try:
            url = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/testdb')
            parsed = urlsplit(url)
            db_name = parsed.path[1:]
        except:
            print "MONGOLAB_URI not properly encoded"
            raise
        '''
        try:
            # Get your DB
            db = Connection(url)[db_name]
        except:
            print "Failed to connect to MONGOLAB database"
            raise

        try:
                db.authenticate(user_pass[0], user_pass[1])
        except:
            print "Failed to authenticate MONGOLAB"
            raise
        
        return db

# Determine what to do
if url==None:
    connectToDatabase.LOCAL=True
else:
    connectToDatabase.LOCAL=False




    

def getCollection(collection_name):
    """ Get a collection from the database

    """
    try:
        db = connectToDatabase()
    except:
        print "_getCollection() - Error: Failed to connect to database"
        raise

    # Check if the 'activities' collection exists:
    if not 'beef' in db.collection_names():
        print "_getCollection() - ERROR: 'beef' collection doesn't exist"
        raise CollectionNotFound("Collection " + collection_name + " Doesn't Exist in Database")

    try:
        beef_collection = db[collection_name]
    except:
        print "_getCollection() - Failed to connect to %s collection" % collection_name
        raise

    return beef_collection


def get_dict_subset(dict, items):
    if items==None: return dict
    beef_dict = OrderedDict()
    for item in items:
        beef_dict[item] = dict[item]
    return beef_dict


def format_dict(beef_dict, items=None):
    """ Format the titles of a return dict

    Reduce the elements in a dict to only the
    items we need, and format them for output

    """

    beef_dict = get_dict_subset(beef_dict, items)
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


#
# Database cleaning functions
#


def _clean_user_database():
    """ Find all invalid beefs for this user and remove their references.
    
    This is to be done from the command-line only

    """

    # Get the user item
    user_coll = getCollection("users")
    beef_coll = getCollection("beef")
    #user = user_coll.find_one({"username" : username})
    user_records = user_coll.find()

    for user in user_records:

        beef_list = user["beef"]
        updated_list = []

        for entry_id in beef_list:
        
            beef_entry = beef_coll.find_one({"_id": entry_id})
            if beef_entry != None:
                updated_list.append(entry_id)
            else:
                print "WARNING: Found an invalid beef id: ", entry_id
                print "Removing from user's list"

            pass

        user["beef"] = updated_list
    
        if user["comments"] == [ [ ] ]:
            user["comments"] = []

            if user["votes"] == []:
                user["votes"] = {}
    
        user_coll.save(user)

    return
    


def _clean_dead_comments(beef_id):
    """ Find all invalid commentss for this beef and remove their references.
    
    This is to be done from the command-line only

    """

    # Get the beef item
    beef_coll = getCollection("beef")
    beef_entry = beef_coll.find_one({"_id" : bson.objectid.ObjectId(beef_id)})
    comment_list = beef_entry["CommentList"]
    
    comments_coll = getCollection("comments")

    updated_list = []

    for comment_id in comment_list:
        
        comment_entry = comments_coll.find_one({"_id": comment_id})
        if comment_entry != None:
            updated_list.append(comment_id)
        else:
            print "WARNING: Found an invalid comment id: ", comment_id
            print "Removing from comment list"
        pass

    beef_entry["CommentList"] = updated_list
    beef_coll.save(beef_entry)


def _clean_beef_entries():
    """ Loop over all beefs and ensure
    that their opponents are valid.

    If the opponent is a username, add
    his id to the db

    Check that the number of votes is
    actually a number

    """

    beef_coll = getCollection("beef")
    users_coll = getCollection("users")

    # Get an iterator over the beef records
    beef_records = beef_coll.find()

    for beef in beef_records:
        
        # Fix the vote numbers
        votes_for = beef.get("VotesFor")
        if votes_for==None or votes_for==[]:
            print "Fixing Votes For: ", votes_for
            beef["VotesFor"] = 0
            
            
        votes_against = beef.get("VotesAgainst")
        if votes_against==None or votes_against==[]:
            print "Fixing Votes Against: ", votes_against
            beef["VotesAgainst"] = 0

        # Check who the beef is against
        beef_opp = beef.get("BeefOpponent")
        if beef_opp != None:

            # Get the opponent's user entry
            user_opp = users_coll.find_one({"username":beef_opp})
            if user_opp == None:
                print "Beef Opponent: %s is not an actual user" % beef_opp
                continue

            user_id = user_opp.get("_id")

            opp_id = beef.get("BeefOpponentId")
            if opp_id == None:
                print "Setting Opponent Id for: ", beef_opp
                beef["BeefOpponentId"] = user_id 
            else:
                print "Found opponent id:", opp_id
                if opp_id != user_id:
                    print "Error: mismatch between user id and beef id"
                    print opp_id, user_id
                    print "Going to set the user_id"
                pass

            # Set the new values
            beef["BeefOpponent"] = beef_opp
            beef["BeefOpponentId"] = user_id

        else:
            print "Error: Beef has no opponent: ", beef

        beef_coll.save(beef)


    
