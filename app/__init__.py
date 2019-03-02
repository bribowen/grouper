#!/usr/bin/env python

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
