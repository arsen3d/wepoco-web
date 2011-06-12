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
from arean import Reanalysis
from arfe import RainfallEstimate

#
# HTTP GET with query ?x=ddd.dd&y=ddd.dd&year=yyyy 
# return is json text or jsonp if callback=somefnname
#
class AData(webapp.RequestHandler):
    def get(self):
        self.getArgs()
        rean = Reanalysis('monthRain',self.year,self.yrs,int(self.reanx),int(self.reany)).data
        satrain = RainfallEstimate('rfe',self.year,self.yrs,self.satx,self.saty).getData()
        month = self.mergeMonth(rean, satrain)
        if len(rean) >0:
            retdata = {}
            retdata['monthRain'] = month
            retdata['message'] = ""
            self.returnJson(retdata)
        else:
            self.error(204) # No content. (205, or 500 might be more appropriate)
        return

    
    def mergeMonth(self, r, s):
        # if either array empty then insert None for all entries
        # if both empty return None
        merged = []
        for i in range(len(r)):
            merged.append([r[i][0],[r[i][1],r[i][1],r[i][1]],s[i][1]])
            pass
        return merged

    def getArgs(self):
        self.reanx = float(self.request.get("rx"))
        self.reany = float(self.request.get("ry"))
        self.satx = float(self.request.get("sx"))
        self.saty = float(self.request.get("sy"))
        self.year = int(self.request.get("year"))
        if self.request.get("yrs"):
            self.yrs = int(self.request.get("yrs"))
        else:
            self.yrs = 1
            pass
        self.callback = self.request.get("callback")
        return

    def returnJson(self,retdata):
        if self.callback:
            self.response.headers['Content-type'] = 'application/javascript'
        else:
            self.response.headers['Content-type'] = 'text/json'
            pass
        if self.callback:
            self.response.out.write("%s(" % self.callback)
            pass
        self.response.out.write(simplejson.dumps(retdata))
        if self.callback:
            self.response.out.write(");")
            pass
        return
