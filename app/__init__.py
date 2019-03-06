#!/usr/bin/env python

from flask import Flask
from config import Config
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config.from_object(Config)
app.config['MYSQL_DATABASE_USER'] = 'grouper'
app.config['MYSQL_DATABASE_PASSWORD'] = 'grouper'
app.config['MYSQL_DATABASE_DB'] = 'grouper'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


from app import routes

if __name__ == "__main__":
    app.run()