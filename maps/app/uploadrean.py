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

class ReanalysisMonth(db.Expando):
    y = db.IntegerProperty(required=True)
    x = db.IntegerProperty(required=True)
    startDate = db.DateProperty(required=True)
    # Use Expando dynamic property for this
    #monthRain = db.ListProperty(int)
    pass

class UploadReanHandler(webapp.RequestHandler):
    def post(self):
        data = simplejson.loads(self.request.get('jsonData'))
        # Or request.raw_post_data might be useful.
        for e in data['rainrecs']:
            lat = data['lats'][e['laidx']]
            lng = data['lons'][e['loidx']]
            txt = "%d,%d %f,%f" % (e['laidx'],e['loidx'],lat,lng)
            logging.info(txt)
            r = ReanalysisMonth(x=e['loidx'],y=e['laidx'],
                 startDate=datetime.strptime(e['first'],"%Y/%m/%d").date(),
                 monthRain=e['rain'])
            r.put()
        self.response.out.write(data)


