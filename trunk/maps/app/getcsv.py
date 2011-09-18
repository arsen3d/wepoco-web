#!/usr/bin/python
# Michael Saunby. September 2011.
# $$
#

#
# Make async calls for JSON data and return a single merged CSV file.
# Enable user of a web form to download composite data.

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from django.utils import simplejson as json

import logging

def handle_result(rpc):
    result = rpc.get_result()
    if result.status_code == 200:
        data = json.loads(result.content)
        logging.debug(data.keys())
    return

# Use a helper function to define the scope of the callback.
def create_callback(rpc):
    return lambda: handle_result(rpc)

class GetCSV(webapp.RequestHandler):
    def get(self):
        try:
            self.getArgs()
            logging.debug("x,y " + x + "," +y) 
            self.download()
        except:
            logging.debug("download failed")
            pass
        return
    
    def getArgs(self):
        global x, y, q0, q1, yr0, yr1, mo
        # treat all as strings
        x = self.request.get("x")
        y = self.request.get("y")
        q0 = self.request.get("q0")
        q1 = self.request.get("q1")
        yr0 = self.request.get("yr0")
        yr1 = self.request.get("yr1")
        mo  = self.request.get("mo")
        return

    def download(self):
        rpcs = []
        for q in [q0,q1]:
            rpc = urlfetch.create_rpc()
            rpc.callback = create_callback(rpc)
            url = "http://saunby.net/cgi-bin/py/series20cr.py?x=%s&y=%s&q=%s&yr0=%s&yr1=%s&mo=%s" % (x,y,q,yr0,yr1,mo)
            urlfetch.make_fetch_call(rpc, url)
            rpcs.append(rpc)
            pass
        # Finish all RPCs, and let callbacks process the results.
        logging.debug("Waiting...")
        for rpc in rpcs:
            rpc.wait()
            pass
        

