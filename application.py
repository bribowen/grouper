#!/usr/bin/env python

#This file is solely used to designate where the application lies. Necessary for deploying with WSGI.

from app import app as application
from app.models import Profile, Project