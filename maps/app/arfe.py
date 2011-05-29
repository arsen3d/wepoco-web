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
from django.utils import simplejson

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
        
#
# HTTP GET with query ?x=ddd.dd&y=ddd.dd&year=yyyy 
# return is json text or jsonp if callback=somefnname
#
class ARfe(webapp.RequestHandler):
    message = "ARfe:"
    dekadname = "dekadrain"
    monthname = "monthrain"
    paramname = "rfe"

    def get(self):
        self.getArgs()
        self.xtile = int(self.x/100)
        self.ytile = int(self.y/100)
        if self.findBlobkey(self.year,self.xtile,self.ytile):
            self.xoff = int(self.x - (100*self.xtile))
            self.yoff = int(self.y - (100*self.ytile))
            b = self.readBlob(self.xoff,self.yoff)
            self.scaleData()
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

    def makeMonth(self):
        monthrain = []
        dk = Dekad(self.year,1,1)
        for i in range(len(self.data)/3):
            edat = self.data[i*3]+self.data[i*3+1]+self.data[i*3+2]
            monthrain.append([dk.str(),[edat,edat,edat]])
            dk.incr(3)
            pass
        self.retdata[self.monthname] = monthrain
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

        self.retdata = {}
        self.retdata[self.dekadname] = dekadrain
        self.makeMonth()
        self.retdata['message'] = "min:%d v:%d" % (self.dmin[0],self.data[0])
        if self.callback:
            self.response.out.write("%s(" % self.callback)
            pass
        self.response.out.write(simplejson.dumps(self.retdata))
        if self.callback:
            self.response.out.write(");")
            pass
        return

    def findBlobkey(self, year, xtile, ytile):
        q = db.GqlQuery("SELECT * FROM DekadTile WHERE year=:1 AND x=:2 AND y=:3 AND param=:4",
                         year,xtile,ytile,self.paramname)
        results = q.fetch(1)
        if len(results):
            self.datakey=results[0].data
            self.dminkey=results[0].dmin
            self.dmaxkey=results[0].dmax
            return True
        return False

    def scaleData(self):
        return

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

class ANdvi(ARfe):
    message = "ANdvi:"
    dekadname = "dekadndvi"
    monthname = "monthndvi"
    paramname = "ndvi"
    def scaleData(self):
        ndata = []
        nmin = []
        nmax = []
        for i in range(len(self.data)):
            if self.data[i] > 250:
                ndata.append(None)
            else:
                ndata.append(self.data[i] / 250.0)
                pass
            pass
        for i in range(len(self.dmin)):
            if self.dmin[i] > 250:
                nmin.append(None)
            else:
                nmin.append(self.dmin[i] / 250.0)
                pass
            pass
        for i in range(len(self.dmax)):
            if self.dmax[i] > 250:
                nmax.append(None)
            else:
                nmax.append(self.dmax[i] / 250.0)
                pass
            pass
        self.data = ndata
        self.dmin = nmin
        self.dmax = nmax
    pass

    # makeMonth is applied after scaleData()
    def makeMonth(self):
        month = []
        dk = Dekad(self.year,1,1)
        for i in range(len(self.data)/3):
            if (self.data[i*3] == None) or (self.data[i*3+1] == None) or (self.data[i*3+2] == None):
                mean = None
            else:
                mean = (self.data[i*3]+self.data[i*3+1]+self.data[i*3+2])/3
                pass
            minval = min([self.data[i*3],self.data[i*3+1],self.data[i*3+2]])
            maxval = max([self.data[i*3],self.data[i*3+1],self.data[i*3+2]])
            month.append([dk.str(),[minval,mean,maxval]])
            dk.incr(3)
            pass
        self.retdata[self.monthname] = month
        return


class checkArfe(webapp.RequestHandler):
    def get(self):
        self.year = int(self.request.get("year"))
        self.callback = self.request.get("callback")
        q = db.GqlQuery("SELECT * FROM DekadTile WHERE year=:1",year)