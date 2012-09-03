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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/MyBeef')
def my_beef():
    return render_template('my_beef.html')

@app.route('/latest_beef', methods=['GET', 'POST'])
def latext_beef():
    """ Get a list of the lastest beef topics

    """
    response = beef.latest()
    return response

@app.route('/get_beef', methods=['GET', 'POST'])
def get_beef():
    """ Get a specific beef topic

    """
    response = beef.get()
    return response

@app.route('/submit_beef', methods=['GET', 'POST'])
def submit_beef( ):
    """ Submit a new beef activity to the db

    """
    response = beef.submit()
    return response

@app.route('/update_beef', methods=['GET', 'POST'])
def update_beef( ):
    """ Update an activity in the db

    """
    response = beef.update()
    return response

@app.route('/delete_beef', methods=['GET', 'POST'])
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
    

