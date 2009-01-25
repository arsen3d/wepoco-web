#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.api import urlfetch, images
from google.appengine.ext import webapp
from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring

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
        data = Element( 'data' )
        date = SubElement( data, 'date' )
        date.text = "20090101"
        self.response.headers['Content-type'] = 'text/xml'
        #self.response.headers['Content-length'] = "%d"%len(rstr)
        ElementTree( data ).write( self.response.out )
        return

