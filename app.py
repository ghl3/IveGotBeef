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
def my_beef():
    return render_template('create_beef.html')


# API:

@app.route('/api/latest_beef', methods=['GET', 'POST'])
def latext_beef():
    """ Get a list of the lastest beef topics

    """
    response = beef.latest()
    return response

@app.route('/api/create_beef', methods=['GET', 'POST'])
def submit_beef( ):
    """ Create a new beef activity to the db

    """
    response = beef.create_beef(request)
    return response

@app.route('/api/get_beef', methods=['GET', 'POST'])
def get_beef():
    """ Get a specific beef topic

    """
    response = beef.get()
    return response

@app.route('/api/update_beef', methods=['GET', 'POST'])
def update_beef( ):
    """ Update an activity in the db

    """
    response = beef.update()
    return response

@app.route('/api/delete_beef', methods=['GET', 'POST'])
def delete_beef( ):
    """ Delete a beef activity

    """
    response = beef.delete()
    return response

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    

