#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.api import urlfetch, images
from google.appengine.ext import webapp
from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring

class MapTile(db.Model):
    name = db.StringProperty()
    png = db.BlobProperty()



class Store(webapp.RequestHandler):
    def post(self):
        maptile = MapTile()
        maptile.name = self.request.get("name")
        img = self.request.get("img")
        maptile.png = db.Blob(img)
        maptile.put()
        self.redirect('/')

class GetTile(webapp.RequestHandler):
    def get(self):
        query = db.Query(MapTile)
        query.filter('name = ',self.request.get("name"))
        result = query.fetch(limit=1)
        maptile = result[0]
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(maptile.png)
