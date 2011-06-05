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

class Reanalysis:
    startYear = 2000
    def __init__(self,paramname,year,yrs,x,y):
        q = db.GqlQuery("SELECT * FROM ReanalysisMonth WHERE startDate=DATE(:1,1,1) AND x=:2 AND y=:3",
                         self.startYear,x,y)
        result = q.fetch(1)
        if len(result):
            rawList = getattr(result[0],paramname)
            outarr=[]
            date = result[0].startDate
            date = date.replace(year=year)
            offsetyrs = year - self.startYear
            selected = rawList[12*offsetyrs:12*(yrs+offsetyrs)]
            for entry in selected:
                outarr.append([date.strftime("%Y/%m/%d"),entry])
                if date.month < 12:
                    month = date.month + 1
                    year = date.year
                else:
                    month = 1
                    year = date.year + 1
                    pass
                date = date.replace(year,month,1)
            pass
            self.data = outarr
        else:
            self.data = []
        pass

#
# HTTP GET with query ?x=ddd.dd&y=ddd.dd&year=yyyy 
# return is json text or jsonp if callback=somefnname
#
class ARean(webapp.RequestHandler):
    paramname = "monthRain"
    startYear = 2000
    def get(self):
        self.getArgs()
        self.data = Reanalysis(self.paramname,self.year,self.yrs,self.x,self.y).data
        if len(self.data) >0:
            self.returnJson()
        else:
            self.error(204) # No content. (205, or 500 might be more appropriate)
        return
    
    def getArgs(self):
        self.x = int(self.request.get("x"))
        self.y = int(self.request.get("y"))
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

