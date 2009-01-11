#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.api import urlfetch, images
from google.appengine.ext import webapp

site = 'wepoco.s3.amazonaws.com'
prefix = '/'

class LatestRainEstimate(webapp.RequestHandler):
    def get(self):
        self.getArgs()
        return
    
    def getArgs(self):
        global x, y, z, mapname, typename
        x = int(self.request.get("x"))
        y = int(self.request.get("y"))
        z = int(self.request.get("zoom"))
        mapname = self.request.get("map")
        typename = self.request.get("type")
        return


