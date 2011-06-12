#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.ext import webapp
from google.appengine.ext import db
from datetime import datetime
# Using simplejson as json library not available in App Engine 
# - they're equivalent.
from django.utils import simplejson
import logging

class StationMonth(db.Expando):
    id = db.StringProperty(required=True)
    year = db.IntegerProperty(required=True)
    # Use Expando dynamic property for this
    #monthRain = db.ListProperty(int)
    pass

class UploadStnRainHandler(webapp.RequestHandler):
    def post(self):
        e = simplejson.loads(self.request.get('jsonData'))
        m = StationMonth(id=e['id'],year=e['year'],monthRain=e['monthRain'])
        m.put()
        self.response.out.write("Done %s %d" % (e['id'],e['year']))
