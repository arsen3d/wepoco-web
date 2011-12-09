#!/usr/bin/python
# Michael Saunby. December 2011.
# $$
#
# Returns reanalysis data for timeseries at specified lat/lng.
# Make async calls for JSON data and return a single merged file.
#
# Only tested with gviz20cr.py as a datasource.  Note that the format of the CSV file
# needs to be just right. For example this is good: 
# "Date","prate" 
# But
# "Date", "prate" 
# is bad.  Seperator must be a single character, not " ,"
#
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from django.utils import simplejson as json
import csv
import logging
# gviz_api.py available here http://code.google.com/p/google-visualization-python/
import gviz_api
import StringIO

def handle_result(rpc):
    result = rpc.get_result()
    if result.status_code == 200:
        logging.debug("HAVE A RESULT")
        logging.debug(result.content[0:30])
        logging.debug(result.headers)
        csvlist.append(result.content)
        pass
    else:
        logging.debug("FAILED TO GET RESULT")
        logging.debug(result.status_code)
        logging.debug(result.content)
    return


# Use a helper function to define the scope of the callback.
def create_callback(rpc):
    return lambda: handle_result(rpc)

class GetMetData(webapp.RequestHandler):
    def get(self):
        logging.debug("getting args...") 
        self.getArgs()
        logging.debug("got args")
        logging.debug("tqx=" + tqx)
        self.download()
        self.returnData(tqx)
        return

    def returnData(self,tqx):
        self.response.headers['Content-type'] = 'text/plain'
        merged = self.merge(csvlist)
        self.response.out.write(json.dumps(merged))
        return
        
    # Merge will combine all second columns with first column of first dataset
    # This assumes that all datasets are of same length and column 1 of each row
    # is the same for all datasets.  
    # Could test for this, but the intended use of this code is pretty narrow.
    # A low cost check would be to ensure first column of first row of all datsets
    # is the same,  i.e. all start at same time, and all have same number or rows.
    def merge(self, csvs):
        # Parse the CSV content
        dsets = []
        logging.debug("Have %d CSV files to merge" % len(csvs))
        for data in csvs:
            content = csv.reader(StringIO.StringIO(data), quoting=csv.QUOTE_NONNUMERIC)
            data = []
            for row in content:
                data.append(row)
                pass
            dsets.append(data)
            logging.debug("First row")
            logging.debug(data[0])
            pass
        # Now merge the data
        merged = dsets[0]
        cols = len(dsets) - 1
        logging.debug("Have %d extra cols" % cols)
        for col in range(cols):
            i = 0
            for row in merged:
                row.append(dsets[col+1][i][1])
                i += 1
                pass
            pass
        logging.debug("Merged")
        logging.debug(merged[0])
        return merged

    def getArgs(self):
        global tqx, lat, lng, fi, start, end
        # treat all as strings
        tqx=self.request.get("tqx")
        lat = self.request.get("lat")
        lng = self.request.get("lng")
        fi = self.request.get("fi")
        start = self.request.get("start")
        end = self.request.get("end")
        return

    def download(self):
        global csvlist
        csvlist = []
        rpcs = []
        (yr0,mo0,dy0) = start.split('-')
        (yr1,mo1,dy1) = end.split('-')
        for q in fi.split(','):
            logging.debug("Fetching " + q)
            rpc = urlfetch.create_rpc(deadline=30) # 60 secs is max, 5 secs is default see 
            # http://code.google.com/appengine/docs/python/urlfetch/asynchronousrequests.html
            rpc.callback = create_callback(rpc)
            url = "http://saunby.net/cgi-bin/py/gviz20cr.py?tqx=out:csv&lat=%s&lng=%s&fi=%s&yr0=%s&mo0=%s&yr1=%s&mo1=%s" % (lat,lng,q,yr0,mo0,yr1,mo1)
            urlfetch.make_fetch_call(rpc, url)
            rpcs.append(rpc)
            pass
        # Finish all RPCs, and let callbacks process the results.
        for rpc in rpcs:
            logging.debug("waiting")
            rpc.wait()
            pass
        
#
# Run the CGI handler.  Share this with other scripts if there's more going on than
# the above.

import wsgiref.handlers

application = webapp.WSGIApplication([  
  ('/getmetdata', GetMetData),
], debug=True)

def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
