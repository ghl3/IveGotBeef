#!/usr/bin/env python

import os
import json
import traceback

from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import jsonify
from flask import flash
from flask import redirect

from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import logout_user

#from Flask_Login import *
#import flask_login
#from flask.ext.login import UserMixin

import pymongo

from common import *

import beef
import login_tools

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.setup_app(app)



# Public Pages:

@app.route('/')
def index():
    
    try:
        beef_list = beef.latest(10)
    except:
        print traceback.format_exc()
        return render_template('500.html')
        
    return render_template('index.html', beef_list=beef_list )


@app.route('/MyBeef')
@login_required
def my_beef():
    """ Render a list of beefs created by the current user

    """
    #if not current_user.is_authenticated():
    #    return render_template('login.html')

    try:
        beef_list = beef.get_beef_list(current_user.id) 
    except:
        print traceback.format_exc()
        return render_template('500.html')
        #return render_template('my_beef.html', beef_list=[])

    return render_template('my_beef.html', beef_list=beef_list),


@app.route('/CreateBeef')
@login_required
def create_beef():
    """ Create a new beef

    """
    return render_template('create_beef.html')


@app.route('/Beef', methods=['GET'])
def get_beef():
    """ Show a particular beef

    """
    try:
        _id = request.args.get('_id', '')
        (beef_dict, comment_list, kwargs) = beef.get_beef(_id)
    except InvalidUser, InvalidBeef:
        print traceback.format_exc()
        return render_template('404.html')
    except:
        print traceback.format_exc()
        return render_template('500.html')

    return render_template('get_beef.html', beef_dict=beef_dict,
                           comment_list=comment_list, **kwargs)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/NewUser", methods=["GET", "POST"])
def new_user():
    registration_form = login_tools.RegistrationForm()
    return render_template("new_user.html", form=registration_form)

#
# Ajax requests
#

@app.route('/api/latest_beef', methods=['GET', 'POST'])
def api_latest_beef():
    """ Get a list of the lastest beef topics

    """
    try:
        response = beef.latest()
    except:
        print traceback.format_exc()
        return jasonify(flag=1)

    return response


@app.route('/api/create_beef', methods=['GET', 'POST'])
@login_required
def api_submit_beef( ):
    """ Create a new beef activity to the db

    """
    try:
        response = beef.create_beef(request)
    except:
        print traceback.format_exc()
        return jsonify(flag=1)

    return response


@app.route('/api/get_beef', methods=['GET', 'POST'])
def api_get_beef():
    """ Get a specific beef topic

    """
    try:
        response = beef.get()
    except:
        print traceback.format_exc()
        return jsonify(flag=1)

    return response


@app.route('/api/update_beef', methods=['GET', 'POST'])
@login_required
def api_update_beef( ):
    """ Update an activity in the db

    """
    try:
        response = beef.update()
    except:
        print traceback.format_exc()
        return jsonify(flag=1)

    return response


@app.route('/api/delete_beef', methods=['GET', 'POST'])
@login_required
def api_delete_beef( ):
    """ Delete a beef activity

    """
    try:
        response = beef.delete()
    except:
        print traceback.format_exc()
        return jsonify(flag=1)
        
    return response


@app.route('/api/add_user', methods=['GET', 'POST'])
def api_add_user( ):
    """ Add a user to the database

    """
    print "Adding User"
    if request.method != 'POST':
        print "Error: Requires POST requiest"
        return jsonify(flag=1)

    try:
        form = login_tools.RegistrationForm(request.form)
        if form.validate():
            response = login_tools.add_user(form)
        else:
            return jsonify(flag=1, message="Form Is Invalid")
    except:
        print traceback.format_exc()
        return jsonify(flag=1)

    return response

#
# User Management
#

@login_manager.user_loader
def load_user(id):
    """ Map the login manager's method to a db check
    
    """

    try:
        response = login_tools._check_db(id)
    except:
        print traceback.format_exc()
        return jsonify(flag=1)

    return response


@app.route("/api/logout")
@login_required
def api_logout():
    """ Logout the current user, forward to current page if possible

    """
    try:
        logout_user()
    except:
        print "Logout Failed!!"
        print traceback.format_exc()
    else:
        print "Successfully Logged out"

    return redirect("/")


@app.route("/api/login", methods=["GET", "POST"])
def api_login():
    """ Login a user and store session with flask_login

    """
    try:
        result = login_tools.login_user_request(request)
    except:
        print traceback.format_exc()
        return jsonify(flag=1)

    return result


@app.route("/api/vote_for", methods=["GET", "POST"])
@login_required
def api_vote_for():
    """ Send a user's vote to the database, updating all necessary entries

    """
    try:
        beef_id = request.form["beef_id"]
        vote_for = request.form["vote_for"]
        user_id = current_user.get_id()
        result = beef.vote(beef_id=beef_id, user_id=user_id, vote_for=vote_for)
    except:
        print traceback.format_exc()
        return jsonify(flag=1)

    return result


@app.route("/api/add_comment", methods=["GET", "POST"])
@login_required
def api_add_comment():
    """ Send a user's vote to the database, updating all necessary entries

    """
    try:
        raise Exception("CHARLES NO!!!!!!!")
        comment = request.form["comment"]
        beef_id = request.form["beef_id"]
        user_id = current_user.get_id()
        result = beef.add_comment(user_id=user_id, beef_id=beef_id, comment=comment)
    except:
        print traceback.format_exc()
        return jsonify(flag=1)

    return result

#
# Errors
#

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
        return render_template('500.html'), 500


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    

