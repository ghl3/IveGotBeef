#!/usr/bin/env python

import os
import json

from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import jsonify
from flask import flash

from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import current_user

#from Flask_Login import *
#import flask_login
#from flask.ext.login import UserMixin

import pymongo
import bson.objectid

import beef

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

login_manager = LoginManager()
login_manager.setup_app(app)

# Public Pages:

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/LatestBeef')
def latest_beef():
    # Get the list of activities 
    beef_list = beef.latest()
    # Return the html with the activities rendered
    return render_template('latest_beef.html', beef_list=beef_list )

@app.route('/MyBeef')
@login_required
def my_beef():
    return render_template('my_beef.html')

@app.route('/CreateBeef')
def create_beef():
    return render_template('create_beef.html')

@app.route('/Beef', methods=['GET'])
def get_beef():
    print "At get_beef()"
    print request.args
    print request.args.get('_id', '')
    _id = request.args.get('_id', '')
    beef_dict = beef.get_beef(_id=_id)
    return render_template('get_beef.html', beef_dict=beef_dict)

#
#
#

@login_manager.user_loader
def load_user(id):
    return beef._check_db(id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]

        '''
        # check MongoDB for the existence of the entered username
        db_result = users_collection.find_one({ 'username' : username })
        
        result_id = int(db_result['userid'])
        
        # create User object/instance
        User = UserClass(db_result['username'], result_id, active=True)
        '''

        User = beef._get_user(username)

        # if username entered matches database, log user in
        if username == user.name: #db_result['username']:
            login_user(User, remember=True)
            return url_for("index")
        else:
            flash("Invalid username.")
    else:
        flash(u"Invalid login.")
        #return render_template("login.html", current_user=current_user)
        return render_template("login.html")
#
#
#
'''
# User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)
'''

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# API:

@app.route('/api/latest_beef', methods=['GET', 'POST'])
def api_latest_beef():
    """ Get a list of the lastest beef topics

    """
    response = beef.latest()
    return response

@app.route('/api/create_beef', methods=['GET', 'POST'])
def api_submit_beef( ):
    """ Create a new beef activity to the db

    """
    response = beef.create_beef(request)
    return response

@app.route('/api/get_beef', methods=['GET', 'POST'])
def api_get_beef():
    """ Get a specific beef topic

    """
    response = beef.get()
    return response

@app.route('/api/update_beef', methods=['GET', 'POST'])
def api_update_beef( ):
    """ Update an activity in the db

    """
    response = beef.update()
    return response

@app.route('/api/delete_beef', methods=['GET', 'POST'])
def api_delete_beef( ):
    """ Delete a beef activity

    """
    response = beef.delete()
    return response

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    

