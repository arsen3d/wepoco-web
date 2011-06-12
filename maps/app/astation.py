#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.ext import webapp
from google.appengine.ext import db
from array import array
# Using simplejson as json library not available in App Engine 
# - they're equivalent.
from django.utils import simplejson
import logging

class StationRain:
    def __init__(self,year,yrs,id):
        outarr=[]
        for yinc in range(yrs):
            q = db.GqlQuery("SELECT * FROM StationMonth WHERE year=:1 AND id=:2",
                            year+yinc,id)
            result = q.fetch(1)
            if len(result):
                rawList = getattr(result[0],'monthRain')
            else:
                rawList = [None,None,None,None,None,None,None,None,None,None,None,None]
                pass
            mon = 1
            for entry in rawList:
                outarr.append(["%d/%02d/01" % (year+yinc,mon),entry])
                mon += 1
                pass
            pass
        self.data = outarr
        return
#
#
class AStnRain(webapp.RequestHandler):
    paramname = "monthRain"
    startYear = 2000
    def get(self):
        self.getArgs()
        self.data = StationRain(self.year,self.yrs,self.id).data
        if len(self.data) >0:
            self.returnJson()
        else:
            self.error(204) # No content. (205, or 500 might be more appropriate)
        return
    
    def getArgs(self):
        self.id = self.request.get("id")
        self.year = int(self.request.get("year"))
        if self.request.get("yrs"):
            self.yrs = int(self.request.get("yrs"))
        else:
            self.yrs = 1
            pass
        self.callback = self.request.get("callback")
        return

    def returnJson(self):
        if self.callback:
            self.response.headers['Content-type'] = 'application/javascript'
        else:
            self.response.headers['Content-type'] = 'text/json'
            pass
        self.retdata = {}
        self.retdata[self.paramname] = self.data
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

