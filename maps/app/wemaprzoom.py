# Author: Michael Saunby.
# 
# Purpose. Generate zoomed map tile on the fly for WeMapr

#import sys, httplib
#import Image, ImageDraw
#import cStringIO
#import cgi

from google.appengine.api import urlfetch, images
from google.appengine.ext import webapp
from StringIO import StringIO

site = 'wemapr.s3.amazonaws.com'
prefix = ''

outcols = 256
outrows = 256
inrows = 256
incols = 256

contenttype = "image/png"

class WemaprZoom(webapp.RequestHandler):
    def get(self):
        self.getArgs()
        self.zoom()
        return

    def getArgs(self):
        global x, y, z, mapname, ref_zoom
        x = int(self.request.get("x"))
        y = int(self.request.get("y"))
        z = int(self.request.get("zoom"))
        ref_zoom = int(self.request.get("ref"))
        mapname = self.request.get("map")


        return

    def download(self, url_fname ):
        urlres = urlfetch.fetch( url_fname )
        if urlres.status_code != 200:
            return None
        return urlres.content

    def zoom(self):
        tile_x = x / (2** (z - ref_zoom))
        tile_y = y / (2** (z - ref_zoom))
        imgname = "%s/%d/%d_%d.png" % (mapname,ref_zoom,tile_x,tile_y)
        #imgname =  "http://" + site + "/" + imgname;
        imgstream = self.download( imgname ) 
        inpic = images.Image(imgstream)
        width = height = 256 / (2** (z - ref_zoom))
        xoffset = width * (x % (2** (z - ref_zoom)))
        yoffset = height * (y % (2** (z - ref_zoom)))
        outpic = images.Image(imgstream)
        outpic.crop( float(xoffset)/incols, float(yoffset)/inrows, float(xoffset + width)/incols, float(yoffset + height)/inrows )
        outpic.resize( outcols,outrows )
        self.response.headers['Content-Type'] = "image/png";
        self.response.out.write( outpic.execute_transforms() )
        return


