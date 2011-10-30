#!/usr/bin/env python
# Michael Saunby.  August 2011.
#
# Purpose:
# Fetch data from OPeNDAP server.
# Either PNG image or JSONP return depending on args.
#

import pydap.lib
pydap.lib.CACHE = "/tmp/pydap-cache/"

from datetime import datetime, tzinfo, timedelta, date
from coards import from_udunits, to_udunits
import numpy
import csv
try:
  import json
  from json import encoder
except:
  import simplejson as json
  from simplejson import encoder

encoder.FLOAT_REPR = lambda o: format(o, '.1f')
import sys
import cgi
import urllib, httplib2

class UTC(tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return "UTC" 
    def dst(self, dt):
        return timedelta(0)
    pass

def udDate(time, dataset):
    date = from_udunits(time, dataset.time.units.replace('GMT', '+0:00'))
    return '%d/%02d/%02d' % (date.year, date.month, date.day)

def returnJson(obj,callback=None):
    if callback:
        print 'Content-type: application/javascript\n'
    else:
        print 'Content-type: text/json\n'
        pass

    if callback:
        print "%s(" % callback
        pass
    print json.dumps(obj)
    if callback:
        print ");"
        pass
    return

from config20cr import months20cr
#badc = {}
#badc['hadisst']={
#    'url':"http://cmip-dap.badc.rl.ac.uk/badc/ukmo-hadisst/data/sst/HadISST_sst.nc",
#    'var': 'sst',
#    'en':'C',
#    'convert': lambda data: data[:].astype('float').tolist()
#    }

def main():
    form=cgi.FieldStorage()
    try:
      callback = form["callback"].value
    except:
      callback = None
      pass 
    try:
        t = int(form["t"].value)
    except:
        returnJson({"msg":"t must be integer"},callback)
        return
    try:
        q = form["q"].value
        config = months20cr[q]
    except:
        k =  months20cr.keys()
        returnJson({"msg":"q must be one of " + str(k)},callback)
        return
    try:
      info = form["info"].value
    except:
      info = None
      pass

    from pydap.client import open_url

    dataset = open_url(config['url'])
    varname = config['var']

    if info:
      data = {}
      data["shape"] = dataset[varname].shape
      for k in dataset.keys():
        data[k] = dataset[k].attributes
      returnJson(data,callback)
      return

    palette = [
      [150,150,60],
      [255,255,255],
      [36,0,216],
      [24,28,248],
      [40,87,255],
      [61,135,255],
      [86,176,255],
      [117,211,255],
      [153,235,255],
      [188,249,255],
      [235,255,255],
      [255,255,235],
      [255,241,188],
      [255,214,153],
      [255,172,117],
      [255,120,86],
      [255,61,61],
      [248,39,53],
      [216,20,47],
      [0,0,0]]
    
    s = dataset[varname][t,:,:].array[:] * dataset[varname].scale_factor + dataset[varname].add_offset
    s = config['convert'](s)
    # first select value should be mising value but above rescaling might have messed this up
    # - Investigate!!
    s = numpy.select([s<-10,
                      s<-5,
                      s<-2, s<0, s<2, s<4, s<6, s<8, s<10, s<12, s<14, s<16, s<18, s<22, s<24, s<26, s<28, s<30, s<32],
                     [0,1,  2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], 
                     default = 19)
    s = s.astype('int')
    
    (hei,wid) = s.shape
    import png, StringIO
    w = png.Writer(wid, hei, palette=palette, bitdepth=8)
    st = StringIO.StringIO()
    w.write(st,s)
    
    print "Content-type: image/png\n"
    print st.getvalue()
    return

if __name__ == '__main__':
  main()
