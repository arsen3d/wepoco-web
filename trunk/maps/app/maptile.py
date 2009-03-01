#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.api import urlfetch, images
from google.appengine.ext import webapp, db
from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring
from google.appengine.ext.webapp.util import run_wsgi_app

class MapTile(db.Model):
    name = db.StringProperty()
    png = db.BlobProperty()



class Store(webapp.RequestHandler):
    def post(self):
        maptile = MapTile()
        maptile.name = self.request.get("name").encode('ascii')
        img = self.request.get("img")
        maptile.png = db.Blob(img)
        maptile.put()
        #self.redirect('/tiletest')
        return

class GetTile(webapp.RequestHandler):
    def get(self):
        query = db.Query(MapTile)
        name = self.request.get("name")
        if not name:
            # Name is URL path excluding '/tileget/'
            name = self.request.path[9:]
        query.filter('name = ',name)
        result = query.fetch(limit=1)
        maptile = result[0]
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(maptile.png)
        return

class TestPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""<html><body>
<form action="/tilestore" enctype="multipart/form-data" method="post">
<input type="file" name="img" /><br />
<input type="text" name="name" />
<input type="submit" />
</form>
<p>%s</p>
<p>tiles</p>""" % self.request.path)
        tiles = db.GqlQuery("SELECT * FROM MapTile") 
        for tile in tiles:
            self.response.out.write("""<a href="/tileget?name=%s">%s</a><br />""" 
                                    % (tile.name,tile.name))
            pass
        self.response.out.write("""</body></html>""")
        return

application = webapp.WSGIApplication([
        ('/tiletest.*', TestPage),
        ('/tilestore', Store),
        ('/tileget.*', GetTile)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

    


