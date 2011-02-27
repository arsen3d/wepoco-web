#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext import db
from dekadtile import DekadTile
from array import array
# Using simplejson as json library not available in App Engine 
# - they're equivalent.
import simplejson

class Dekad:
    def __init__(self,startyr,startmo,startdk):
        self.yr = startyr;
        self.mo = startmo;
        self.dk = startdk;
    def incr(self,n=1):
        for i in range(n):
            self.dk += 1
            if self.dk == 4:
                self.dk = 1
                self.mo += 1
                pass
            if self.mo == 13:
                self.mo = 1
                self.yr += 1
                pass
            pass
        return
    def str(self):
        dy = [99,1,11,21]
        return "%4d-%02d-%02d" % (self.yr, self.mo, dy[self.dk])
        

class ARfe(webapp.RequestHandler):
    message = "ARfe:"
    def get(self):
        self.getArgs()
        self.xtile = int(self.x/100)
        self.ytile = int(self.y/100)
        if self.findBlobkey(self.year,self.xtile,self.ytile):
            self.xoff = int(self.x - (100*self.xtile))
            self.yoff = int(self.y - (100*self.ytile))
            b = self.readBlob(self.xoff,self.yoff)
            self.returnJson()
        else:
            self.response.headers['Content-type'] = 'text/json'
            retdata = {}
            retdata['message'] = "Error - no data"
            if self.callback:
                self.response.out.write("%s(" % self.callback)
                pass
            self.response.out.write(simplejson.dumps(retdata))
            if self.callback:
                self.response.out.write(");")
                pass
            pass
        return
    
    def getArgs(self):
        self.x = float(self.request.get("x"))
        self.y = float(self.request.get("y"))
        self.year = int(self.request.get("year"))
        self.callback = self.request.get("callback")
        return

    def returnJson(self):
        self.response.headers['Content-type'] = 'text/json'
        dk = Dekad(self.year,1,1)
        dekadrain = []
        for i in range(len(self.data)):
            edat = self.data[i]
            try:
                emin = self.dmin[i]
            except:
                emax = edat
                pass
            try:
                emax = self.dmax[i]
            except:
                emax = edat
                pass
            dekadrain.append([dk.str(),[emin,edat,emax]])
            dk.incr()
            pass
        dk = Dekad(self.year,1,1)
        monthrain = []
        for i in range(len(self.data)/3):
            edat = self.data[i*3]+self.data[i*3+1]+self.data[i*3+2]
            monthrain.append([dk.str(),edat])
            dk.incr(3)
            pass
        retdata = {}
        retdata['dekadrain'] = dekadrain
        retdata['monthrain'] = monthrain
        retdata['message'] = "min:%d v:%d" % (self.dmin[0],self.data[0])
        if self.callback:
            self.response.out.write("%s(" % self.callback)
            pass
        self.response.out.write(simplejson.dumps(retdata))
        if self.callback:
            self.response.out.write(");")
            pass
        return

    def findBlobkey(self, year, xtile, ytile):
        q = db.GqlQuery("SELECT * FROM DekadTile WHERE year=:1 AND x=:2 AND y=:3",
                         year,xtile,ytile)
        results = q.fetch(1)
        if len(results):
            self.datakey=results[0].data
            self.dminkey=results[0].dmin
            self.dmaxkey=results[0].dmax
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
