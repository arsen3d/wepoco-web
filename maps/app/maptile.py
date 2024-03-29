#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.api import urlfetch, images, memcache
from google.appengine.ext import webapp, db
from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring
from google.appengine.ext.webapp.util import run_wsgi_app
from StringIO import StringIO
import array

class MapTile(db.Model):
    name = db.StringProperty()
    png = db.BlobProperty()

class LutMatrix(db.Model):
    name = db.StringProperty()
    matrix = db.BlobProperty()

class Store(webapp.RequestHandler):
    def post(self):
        maptile = MapTile()
        maptile.name = self.request.get("name").encode('ascii')
        img = self.request.get("img")
        maptile.png = db.Blob(img)
        maptile.put()
        return

class StoreLut(webapp.RequestHandler):
    def post(self):
        lutmatrix = LutMatrix()
        lutmatrix.name = self.request.get("name").encode('ascii')
        lut = self.request.get("lut")
        lutmatrix.matrix = db.Blob(lut)
        lutmatrix.put()
        return


class GetTile(webapp.RequestHandler):
    site = 'http://wepoco.s3.amazonaws.com/mpe/'
    def get(self):
        name = self.request.get("name")
        if not name:
            # Name is URL path excluding '/tileget/'
            name = self.request.path[9:]
        query = db.Query(MapTile)
        query.filter('name = ',name)
        result = query.fetch(limit=1)
        try:
            maptile = result[0]
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(maptile.png)
        except:
            tile_data = self.download( self.site, name )
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(tile_data)
        return

    def download(self, site, name ):
        img_data = memcache.get( site + name )
        if img_data is not None:
            return img_data
        else:
            urlres = urlfetch.fetch( site + name )
            if urlres.status_code != 200:
                return None
            img_data = urlres.content
            memcache.add(site + name, img_data, 3600)
            pass
        # Now store it
        if img_data is not None:
            maptile = MapTile()
            maptile.name = name
            maptile.png = db.Blob(img_data)
            maptile.put()
            pass
        return img_data


class MakeTile(webapp.RequestHandler):
    def get(self):
        src = self.request.get("src")
        dest = self.request.get("dest")
        lut = self.request.get("lut")
        # open the LUT
        query = db.Query(LutMatrix)
        query.filter('name = ',lut)
        havedata = "no"
        try:
            lutdata = query.fetch(limit=1)[0].matrix
            havedata = "yes"
        except:
            pass
        matrix = array.array('h')
        matrix.fromstring(lutdata)
        self.response.out.write("""<html><body>
<p>src = %s</p>
<p>dest = %s</p>
<p>lut = %s</p>
<p>havedata = %s</p>
</html></body>""" % (src,dest,lut,havedata))
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
        ('/tiletest', TestPage),
        ('/tilestore', Store),
        ('/tileget.*', GetTile),
        ('/tilelut', StoreLut),
        ('/tileproj', MakeTile)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

    


