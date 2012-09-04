
import traceback

from beef import _getCollection

from flask import jsonify
from flask.ext.login import UserMixin

import bson.objectid

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class UserClass(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

        def is_active(self):
            return self.active

        #def set_password(self, password):
        #    self.pw_hash = generate_password_hash(password)

        #def check_password(self, password):
        #    return check_password_hash(self.pw_hash, password)


def _check_db(_id):
    """ Check that a user session id is valid

    This is a required method for flask_login
    """
    try:
        users_collection = _getCollection("users")
    except:
        print "Failed to get collection in _check_db"
        raise

    db_check = users_collection.find_one({ '_id' : bson.objectid.ObjectId(_id) })
    UserObject = UserClass(db_check['username'], _id, active=True)

    if UserObject.id == _id:
        return UserObject
    else:
        return None


def add_user(request):
    """ Add a user and pw_hash to the database

    """

    print "Adding user"

    if "username" not in request.form:
        print "Error: 'username' not in request"
        return jsonify(flag=1)

    username = request.form["username"]
    
    #if _user_exists(username):
    #    print "Warning: User already exists"
    #    return jsonify(flag=0, UserAdded="UserAlreadyExists")

    try:
        users_collection = _getCollection("users")
    except:
        print "add_user(): Failed to get collection 'users'"
        print traceback.format_exc()
        return jsonify(flag=1)

    if users_collection.find_one({'username' : username}) != None:
        print "Cannot create use: %s, user already exists" % username
        return jsonify(flag=0, UserAdded=1, Message="User Already Exists")

    pw_hash = generate_password_hash(request.form["password"])
    users_collection.save( {"username": username, "pw_hash": pw_hash} )
    print "Successfully Created user: %s" % username
    return jsonify(flag=0, UserAdded=0)
    return


class InvalidUser(Exception):
    pass

def _authenticate(username, password):

    if not _user_exists(username):
        raise InvalidUser

    try:
        users_collection = _getCollection("users")
    except:
        print "Failed to get collection in _add_user"
        raise

    user = users_collection.find_one({'username' : username})

    if "pw_hash" not in user:
        print "Error: _authenticate() - attribute 'pw_hash' not in user entry in database"
        raise Exception

    if check_password_hash(user["pw_hash"], password):
        print "Successfully authenticated user: %s" % username
        return True
    else:
        print "Incorrect username/password combo for user: %s" % username
        return False


def _user_exists(username):
    """ Query the users database to see if user exists

    Check only the username and see if it matches an entry
    """
    try:
        users_collection = _getCollection("users")
    except:
        print "Failed to get collection in _user_exists"
        raise

    db_check = users_collection.find_one({'username' : username})
              
    if db_check==None:
        return False

    return True


def _get_user(username):

    try:
        users_collection = _getCollection("users")
    except:
        print "Failed to get collection in _get_user"
        raise

    db_result = users_collection.find_one({ 'username' : username })
    result_id = db_result['_id'].__str__()
    
    # create User object/instance
    User = UserClass(db_result['username'], result_id, active=True)

    return User
