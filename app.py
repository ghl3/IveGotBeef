#!/usr/bin/env python

import os
import json

from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import jsonify

import pymongo
import bson.objectid

import beef

app = Flask(__name__)


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
    

