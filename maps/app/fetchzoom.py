#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

#
# Configuration
#

from google.appengine.api import urlfetch, images
from google.appengine.ext import webapp
from StringIO import StringIO

site = 'wepoco.s3.amazonaws.com'
prefix = '/'

ref_zoom = 5
outcols = 256
outrows = 256
inrows = 256
incols = 256

contenttype = "image/png"


class FetchZoom(webapp.RequestHandler):
    def get(self):
        try:
            self.getArgs()
            self.zoom()
        except:
            pass
        return
    
    def getArgs(self):
        global x, y, z, mapname, typename
        x = int(self.request.get("x"))
        y = int(self.request.get("y"))
        z = int(self.request.get("zoom"))
        mapname = self.request.get("map")
        typename = self.request.get("type")
        return

    def download(self, url_fname ):
        urlres = urlfetch.fetch( url_fname )
        if urlres.status_code != 200:
            return None
        return urlres.content

    def zoom(self):
        tile_x = x / (2** (z - ref_zoom))
        tile_y = y / (2** (z - ref_zoom))
        imgname = "%s/%s/%d/%d_%d.png" % (typename,mapname,ref_zoom,tile_x,tile_y)
        imgstream = self.download(  "http://" + site + prefix + imgname ) 
        width = height = 256 / (2** (z - ref_zoom))
        xoffset = width * (x % (2** (z - ref_zoom)))
        yoffset = height * (y % (2** (z - ref_zoom)))
        outpic = images.Image(imgstream)
        outpic.crop( float(xoffset)/incols, float(yoffset)/inrows, float(xoffset + width)/incols, float(yoffset + height)/inrows )
        outpic.resize( outcols,outrows )
        self.response.headers['Content-Type'] = "image/png";
        self.response.out.write( outpic.execute_transforms() )
        return

    def zoom_old(self):
        tile_x = x / (2** (z - ref_zoom))
        tile_y = y / (2** (z - ref_zoom))
        imgname = "%s/%s/%d/%d_%d.png" % (typename,mapname,ref_zoom,tile_x,tile_y)
        imgstream = self.download(  "http://" + site + prefix + imgname ) 
        width = height = 256 / (2** (z - ref_zoom))
        xoffset = width * (x % (2** (z - ref_zoom)))
        yoffset = height * (y % (2** (z - ref_zoom)))
        outpic = images.crop( imgstream, float(xoffset)/incols, float(yoffset)/inrows, float(xoffset + width)/incols, float(yoffset + height)/inrows )
        outpic = images.resize( outpic, outcols,outrows )
        self.response.headers['Content-Type'] = "image/png";
        self.response.out.write( outpic )
        return

