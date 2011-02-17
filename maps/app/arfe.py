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
    def get(self):
        self.getArgs()
        self.returnJson()
        return
    
    def getArgs(self):
        global x
        global y
        global year
        x = float(self.request.get("x"))
        y = float(self.request.get("y"))
        year = int(self.request.get("year"))
        return

    def returnJson(self):
        self.response.headers['Content-type'] = 'text/json'
        dk = Dekad(2010,1,1)
        dekadrain = []
        for e in range(36):
            dekadrain.append([dk.str(),[e-10,e,e+20]])
            dk.incr()
            pass
        retdata = {}
        retdata['dekadrain'] = dekadrain
        retdata['message'] = "x:%f y:%f yr:%d" %  (x, y, year)
        self.response.out.write(simplejson.dumps(retdata));
        return

    def readBlob(self,key,x,y):
        # Data stored in blocks of 100x100
        # Will need to seek to (y*100+x)*ob_size then read ob_size bytes
        # ob_size is 36*2
        ob_size = 72
        pos =  (y*100+x)*ob_size
        blob_reader = blobstore.BlobReader(key, position=pos, buffer_size=ob_size*2)
        data = blob_reader.read(ob_size)
        
        return data

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
