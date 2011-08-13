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
        return "%4d/%02d/%02d" % (self.yr, self.mo, dy[self.dk])


class RainfallEstimate:
    missing = -1024
    def __init__(self,paramname,year,yrs,x,y):
        self.paramname = paramname
        self.year = year
        self.xtile = int(x/100)
        self.ytile = int(y/100)
        self.xoff = int(x - (100*self.xtile))
        self.yoff = int(y - (100*self.ytile))
        self.data = array('h')
        self.dmin = array('h')
        self.dmax = array('h')
        for iyr in range(yrs):
            if self.findBlobkey(year + iyr,self.xtile,self.ytile,self.paramname):
                self.readBlob()
                pass
            else:
                for dk in range(36):
                    self.data.append(self.missing)
                    self.dmin.append(self.missing)
                    self.dmax.append(self.missing)
                    pass
            pass
        self.month = self.makeMonth()
        return

    def getData(self):
        return self.month

    def makeMonth(self):
        monthrain = []
        dk = Dekad(self.year,1,1)
        for i in range(len(self.data)/3):
            if self.data[i*3] == self.missing:
               monthrain.append([dk.str(),[None,None,None]])
            else:
                edat = self.data[i*3]+self.data[i*3+1]+self.data[i*3+2]
                if edat < 0: edat = None
                emin = edat
                emax = edat
                monthrain.append([dk.str(),[emin,edat,emax]])
                pass
            dk.incr(3)
            pass
        return monthrain

    def findBlobkey(self, year, xtile, ytile, paramname):
        q = db.GqlQuery("SELECT * FROM DekadTile WHERE year=:1 AND x=:2 AND y=:3 AND param=:4",
                         year,xtile,ytile,paramname)
        results = q.fetch(1)
        if len(results):
            self.datakey=results[0].data
            self.dminkey=results[0].dmin
            self.dmaxkey=results[0].dmax
            return True
        return False

    def readBlob(self):
        # Data stored in blocks of 100x100
        # Will need to seek to (y*100+x)*ob_size then read ob_size bytes
        # ob_size is 36*2
        # See http://code.google.com/appengine/docs/python/blobstore/blobreaderclass.html
        x = self.xoff
        y = self.yoff
        ob_size = 36*2
        pos =  (y*100+x)*ob_size
        blob_reader = blobstore.BlobReader(self.datakey,position=pos,buffer_size=ob_size*2)
        self.data.fromstring(blob_reader.read(ob_size))
        blob_reader = blobstore.BlobReader(self.dminkey,position=pos,buffer_size=ob_size*2)
        self.dmin.fromstring(blob_reader.read(ob_size))
        blob_reader = blobstore.BlobReader(self.dmaxkey,position=pos,buffer_size=ob_size*2)
        self.dmax.fromstring(blob_reader.read(ob_size))
        return
    
        
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
        rainEst = RainfallEstimate(self.paramname,self.year,self.yrs,self.x,self.y)
        self.missing = rainEst.missing
        self.dmin = rainEst.dmin
        self.data = rainEst.data
        self.dmax = rainEst.dmax
        self.month = rainEst
        if len(self.data) >0:
            self.scaleData()
            self.returnJson()
        else:
            self.error(204) # No content. (205, or 500 might be more appropriate)
        return
    
    def getArgs(self):
        self.x = float(self.request.get("x"))
        self.y = float(self.request.get("y"))
        self.year = int(self.request.get("year"))
        if self.request.get("yrs"):
            self.yrs = int(self.request.get("yrs"))
        else:
            self.yrs = 1
            pass
        self.callback = self.request.get("callback")
        return

    def scaleData(self):
        return

    def makeMonth(self):
        monthrain = []
        dk = Dekad(self.year,1,1)
        for i in range(len(self.data)/3):
            edat = self.data[i*3]+self.data[i*3+1]+self.data[i*3+2]
            #emin = min([self.data[i*3],self.data[i*3+1],self.data[i*3+2]]) * 3
            #emax = max([self.data[i*3],self.data[i*3+1],self.data[i*3+2]]) * 3
            emin = edat
            emax = edat
            monthrain.append([dk.str(),[emin,edat,emax]])
            dk.incr(3)
            pass
        self.retdata[self.monthname] = monthrain
        return

    def returnJson(self):
        if self.callback:
            self.response.headers['Content-type'] = 'application/javascript'
        else:
            self.response.headers['Content-type'] = 'text/json'
            pass
        dk = Dekad(self.year,1,1)
        dekadrain = []
        for i in range(len(self.data)):
            edat = self.data[i]
            if edat < 0: edat = None
            try:
                emin = self.dmin[i]
                if emin < 0: emin = None
            except:
                emin = edat
                pass
            try:
                emax = self.dmax[i]
                if emax < 0: emax = None
            except:
                emax = edat
                pass
            dekadrain.append([dk.str(),[emin,edat,emax]])
            dk.incr()
            pass

        self.retdata = {}
        self.retdata[self.dekadname] = dekadrain
        self.makeMonth()
        self.retdata['message'] = ""
        if self.callback:
            self.response.out.write("%s(" % self.callback)
            pass
        self.response.out.write(simplejson.dumps(self.retdata))
        if self.callback:
            self.response.out.write(");")
            pass
        return

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
            if self.data[i] == self.missing:
                ndata.append(None)
            elif self.data[i] > 250:
                ndata.append(None)
            else:
                ndata.append(self.data[i] / 250.0)
                pass
            pass
        for i in range(len(self.dmin)):
            if self.dmin[i] == self.missing:
                nmin.append(None)
            elif self.dmin[i] > 250:
                nmin.append(None)
            else:
                nmin.append(self.dmin[i] / 250.0)
                pass
            pass
        for i in range(len(self.dmax)):
            if self.dmax[i] == self.missing:
                nmax.append(None)
            elif self.dmax[i] > 250:
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
                minval = None
                maxval = None
            else:
                mean = (self.data[i*3]+self.data[i*3+1]+self.data[i*3+2])/3
                minval = min([self.data[i*3],self.data[i*3+1],self.data[i*3+2]])
                maxval = max([self.data[i*3],self.data[i*3+1],self.data[i*3+2]])
                pass
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
