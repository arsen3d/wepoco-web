#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.api import urlfetch, images
from google.appengine.ext import webapp
from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring
from datetime import datetime, timedelta

site = 'wepoco.s3.amazonaws.com'
prefix = '/'

class LatestRainEstimate(webapp.RequestHandler):
    def get(self):
        self.getArgs()
        self.returnDate()
        return
    
    def getArgs(self):
        global x
        #x = int(self.request.get("x"))
        return

    def returnDate(self):
        yesterday = datetime.today() - timedelta(1)
        data = Element( 'data' )
        date = SubElement( data, 'date' )
        date.text = "%02d/%02d/%4d" % (yesterday.day,yesterday.month,yesterday.year)
        self.response.headers['Content-type'] = 'text/xml'
        #self.response.headers['Content-length'] = "%d"%len(rstr)
        ElementTree( data ).write( self.response.out )
        return

