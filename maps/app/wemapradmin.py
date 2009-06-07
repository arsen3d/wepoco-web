# Author: Michael Saunby.
# 

from google.appengine.api import urlfetch, images, memcache
from google.appengine.ext import webapp, db
from StringIO import StringIO

from maptile import MapTile

class WemaprAdmin(webapp.RequestHandler):
    def get(self): 
        total = self.getCount()
        self.response.out.write( "<p>MapTile</p>" )
        self.response.out.write( "<p>total = " + str(total) + "</p>" )
        #self.response.headers['Content-Type'] = "image/png";
 
        if total > 500:
            q = self.getOldest(total - 500)
            self.response.out.write( "<p>removing" + str(total - 500) + "</p>" )
            for tile in q:
                tile.delete()
                pass
            pass
        return

    def getCount(self):
        #query = db.Query(MapTile)
        q = db.GqlQuery("SELECT * FROM MapTile") 
        return q.count()

    def getOldest(self, num=1):
        q = db.GqlQuery("SELECT * FROM MapTile ORDER BY name ASC LIMIT " + str(num))
        return q

    def getArgs(self):
        global x, y, z, mapname, ref_zoom
        x = int(self.request.get("x"))
        y = int(self.request.get("y"))
        z = int(self.request.get("zoom"))
        ref_zoom = int(self.request.get("ref"))
        mapname = self.request.get("map")
        return



