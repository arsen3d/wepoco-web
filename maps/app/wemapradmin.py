# Author: Michael Saunby.
# 

from google.appengine.api import urlfetch, images, memcache
from google.appengine.ext import webapp
from StringIO import StringIO

class WemaprAdmin(webapp.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = "image/png";
        self.response.out.write( "hello" )
        return

    def getArgs(self):
        global x, y, z, mapname, ref_zoom
        x = int(self.request.get("x"))
        y = int(self.request.get("y"))
        z = int(self.request.get("zoom"))
        ref_zoom = int(self.request.get("ref"))
        mapname = self.request.get("map")
        return



