
import traceback
import datetime
import json

from flask import jsonify
from flask import redirect
from flask import url_for
from flask.ext.login import UserMixin
from flask.ext.login import login_user
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import logout_user

import bson.objectid

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from common import *

from wtforms import Form, BooleanField, TextField, PasswordField, validators


class UserClass(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

        def is_active(self):
            return self.active


class RegistrationForm(Form):
    FirstName = TextField('First Name', [validators.Required(), validators.Length(min=1, max=25)])
    LastName  = TextField('Last Name',   [validators.Required(), validators.Length(min=1, max=25)])
    username  = TextField('UserName', [validators.Required(), validators.Length(min=4, max=20)])
    email     = TextField('Email Address', [validators.Required(), validators.Length(min=6, max=35), validators.Email()])
    password  = PasswordField('Password', [
            validators.Required(),
            validators.EqualTo('confirm', message='Passwords must match')
            ])
    confirm = PasswordField('Confirm Password', [validators.Required()])


def new_user(user_form):
    """ Add a new user and pw_hash to the database

    """

    print "Adding new user from form"

    # Get the dictionary (Immutable, to be specific)
    # From the WTForm object
    user_dict = user_form.data

    username = user_dict["username"]
    users_collection = getCollection("users")

    if users_collection.find_one({'username' : username}) != None:
        print "Cannot create use: %s, user already exists" % username
        return jsonify(flag=0, UserAdded=1, Message="User Already Exists")

    password = user_dict.pop("password")
    pw_hash = generate_password_hash(password)
    if "confirm" in user_dict:
        del user_dict["confirm"]

    user_dict["pw_hash"] = pw_hash
    user_dict["time_added"] = datetime.datetime.utcnow()
    user_dict["beef"] = [] 
    user_dict["comments"] = {} # Dict of beef_id to comment
    user_dict["votes"] = {} # dict of beef_id to vote
    
    users_collection.save(user_dict)
    print "Successfully Created user: %s" % username
    return jsonify(flag=0, UserAdded=0)
    return


def login_user_request(request):
    """ Take a request object and login a user

    """
    if request.method == "POST" \
            and "username" in request.form \
            and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]

        if not _user_exists(username):
            return jsonify(flag=0, UserLoggedIn=1, Message="User does not exist")

        User = _get_user(username)

        try: 
            authenticated = _authenticate(username, password)
        except InvalidUser:
            print "Warning: Invalid User: %s" % username
            return jsonify(flag=0, UserLoggedIn=1, Message="Invalid User")

        if authenticated:
            login_user(User, remember=True)
            print "Successfully logged in user: %s " % username
            print "Current User: ", current_user, current_user.name, current_user.id
            return jsonify(flag=0, UserLoggedIn=0)
        else:
            print "Failed to login user: %s" % username
            return jsonify(flag=0, UserLoggedIn=1, Message="Failed to log in user")
            flash("Invalid username.")
    else:
        #flash(u"Invalid login.")
        return render_template("login.html")


def _check_db(_id):
    """ Check that a user session id is valid

    This is a required method for flask_login
    """

    users_collection = getCollection("users")

    db_check = users_collection.find_one({ '_id' : bson.objectid.ObjectId(_id) })
    if db_check==None:
        return None
    UserObject = UserClass(db_check['username'], _id, active=True)

    if UserObject.id == _id:
        return UserObject
    else:
        return None


def _authenticate(username, password):

    if not _user_exists(username):
        raise InvalidUser

    users_collection = getCollection("users")
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

    users_collection = getCollection("users")
    db_check = users_collection.find_one({'username' : username})
              
    if db_check==None:
        return False

    return True


def _get_user(username):
    """ Find a user in the db and return a Login class for that user

    """

    users_collection = getCollection("users")
    db_result = users_collection.find_one({ 'username' : username })
    result_id = db_result['_id'].__str__()
    
    # create User object/instance
    User = UserClass(db_result['username'], result_id, active=True)

    return User
