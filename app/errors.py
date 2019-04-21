#!/usr/bin/env python
#This file describes how to handle various errors.

#Importing of necessary libraries/files.
from flask import render_template
from app import app, db

#Handles 404 errors by redirecting to the 404.html file, stored in app/templates/404.html.
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

#Same as the above, but with 500 errors.
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500