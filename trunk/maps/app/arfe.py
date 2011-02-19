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
    def incr(self):
        self.dk += 1
        if self.dk == 4:
            self.dk = 1
            self.mo += 1
            pass
        if self.mo == 13:
            self.mo = 1
            self.yr += 1
            pass
        return
    def str(self):
        dy = [99,1,11,21]
        return "%4d-%02d-%02d" % (self.yr, self.mo, dy[self.dk])
        

class ARfe(webapp.RequestHandler):
    message = "ARfe:"
    def get(self):
        self.getArgs()
        #self.readBlob()
        self.xtile = int(self.x/100)
        self.ytile = int(self.y/100)
        self.findBlobkey(self.year,self.xtile,self.ytile)
        self.xoff = int(self.x - (100*self.xtile))
        self.yoff = int(self.y - (100*self.ytile))
        b = self.readBlob(self.xoff,self.yoff)
        self.message += " read %d " % b
        self.message += "(%d,%d, %d,%d %d)" % (self.xtile, self.xoff, self.ytile, self.yoff, self.year)
        self.returnJson()
        return
    
    def getArgs(self):
        self.x = float(self.request.get("x"))
        self.y = float(self.request.get("y"))
        self.year = int(self.request.get("year"))
        return

    def returnJson(self):
        self.response.headers['Content-type'] = 'text/json'
        dk = Dekad(self.year,1,1)
        dekadrain = []
        for e in self.data:
            dekadrain.append([dk.str(),[e,e,e]])
            dk.incr()
            pass
        retdata = {}
        retdata['dekadrain'] = dekadrain
        retdata['message'] = self.message
        self.response.out.write(simplejson.dumps(retdata));
        return

    def findBlobkey(self, year, xtile, ytile):
        q = db.GqlQuery("SELECT * FROM DekadTile WHERE year=:1 AND x=:2 AND y=:3",
                         year,xtile,ytile)
        results = q.fetch(1)
        if len(results):
            self.blobkey=results[0].data
        return

    def readBlob(self,x,y):
        # Data stored in blocks of 100x100
        # Will need to seek to (y*100+x)*ob_size then read ob_size bytes
        # ob_size is 36*2
        ob_size = 36*2
        pos =  (y*100+x)*ob_size
        blob_reader = blobstore.BlobReader(self.blobkey, 
                                           position=pos, buffer_size=ob_size*2)
        self.data = array('h')
        self.data.fromstring(blob_reader.read(ob_size))
        return len(self.data)

        # See http://code.google.com/appengine/docs/python/blobstore/blobreaderclass.html
        # blob_key = ...

        # Instantiate a BlobReader for a given Blobstore value.

        #blob_reader = blobstore.BlobReader(blob_key)
        
        # Instantiate a BlobReader for a given Blobstore value, setting the
        # buffer size to 1 MB.

        #blob_reader = blobstore.BlobReader(blob_key, buffer_size=1048576)
        
        # Instantiate a BlobReader for a given Blobstore value, setting the
        # initial read position.

        #blob_reader = blobstore.BlobReader(blob_key, position=4194304)
        
        # Read the entire value into memory. This may take a while depending
        # on the size of the value and the size of the read buffer, and is not
        # recommended for large values.

        #value = blob_reader.read()
        
        # Set the read position, then read 100 bytes.

        #blob_reader.seek(2097152)
        #data = blob_reader.read(100)
        
        # Read the value, one line (up to and including a '\n' character) at a time.

        #for line in blob_reader:
        # ...
        return
