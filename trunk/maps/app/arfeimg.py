#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.api import images
from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext import db
from rfepic import RfePic
from array import array

#
# HTTP GET with query ?dek=kk&mon=mm&year=yyyy 
# return is json text or jsonp if callback=somefnname
#
class ARfeImg(webapp.RequestHandler):
    def get(self):
        self.getArgs()
        if self.findBlobkey():
            #self.response.out.write("got it") 
            self.returnImg()
        else:
           self.response.out.write("hello world") 
        return
    
    def getArgs(self):
        self.dekad = int(self.request.get("dek"))
        self.month = int(self.request.get("mon"))
        self.year = int(self.request.get("year"))
        try:
            self.left = float(self.request.get("left"))
            self.top = float(self.request.get("top"))
            self.right = float(self.request.get("right"))
            self.bottom = float(self.request.get("bottom"))
        except:
            self.left = 0.0
            self.top = 0.0
            self.right = 1.0
            self.bottom = 1.0
        return

    def returnImg(self):
        img = images.Image(blobstore.BlobReader(self.fullpic).read())
        img.crop(self.left,self.top,self.right,self.bottom)
        crop = img.execute_transforms() 
        self.response.headers['Content-type'] = 'image/png'
        self.response.out.write(crop)
        return

    def findBlobkey(self):
        q = db.GqlQuery("SELECT * FROM RfePic WHERE year=:1 AND month=:2 AND dek=:3",
                         self.year,self.month,self.dekad)
        results = q.fetch(1)
        if len(results):
            self.fullpic=results[0].pic
            return True
        return False

    def readBlob(self,x,y):
        # Data stored in blocks of 100x100
        # Will need to seek to (y*100+x)*ob_size then read ob_size bytes
        # ob_size is 36*2
        # See http://code.google.com/appengine/docs/python/blobstore/blobreaderclass.html
        ob_size = 36*2
        pos =  (y*100+x)*ob_size
        self.data = array('h')
        try:
            blob_reader = blobstore.BlobReader(self.datakey,position=pos,buffer_size=ob_size*2)
            self.data.fromstring(blob_reader.read(ob_size))
        except: pass
        self.dmin = array('h')
        #try:
        blob_reader = blobstore.BlobReader(self.dminkey,position=pos,buffer_size=ob_size*2)
        self.dmin.fromstring(blob_reader.read(ob_size))
        #except: pass
        self.dmax = array('h')
        try:
            blob_reader = blobstore.BlobReader(self.dmaxkey,position=pos,buffer_size=ob_size*2)
            self.dmax.fromstring(blob_reader.read(ob_size))  
        except: pass
        return len(self.data)
    pass


