#!/usr/bin/env python
# Michael Saunby.  August 2011.
#
# Purpose:
# Fetch rainfall time series for single grid box. 
#

import pydap.lib
pydap.lib.CACHE = "/tmp/pydap-cache/"
from pydap.client import open_url
from datetime import datetime, tzinfo, timedelta, date
from coards import from_udunits, to_udunits
import numpy
import csv
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.1f')
import sys
import cgi

from config20cr import months20cr

class UTC(tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return "UTC" 
    def dst(self, dt):
        return timedelta(0)
    pass

default_year_start = 1961

# Monthly means are assigned to first day of month. That's why the
# range ends on 1st December.

#dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets20thC_ReanV2/" 
#monthly_monolevel = dods + "Monthlies/gaussian/monolevel/"
#precip_rate_url = dods + "gaussian/monolevel/prate.2008.nc"
#precip_month_url = dods + "Monthlies/gaussian/monolevel/prate.mon.mean.nc"

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


def main():
    form=cgi.FieldStorage()
    try:
        x = int(form["x"].value)
        y = int(form["y"].value)
    except:
        returnJson({"msg":"x and y must be integers"})
        return
    try:
        q = form["q"].value
        config = months20cr[q]
    except:
        k =  months20cr.keys()
        returnJson({"msg":"q must be one of " + str(k)})
        return
    try:
        year_start = int(form["yr0"].value)
    except:
        year_start = default_year_start
        pass
    try:
        year_end = int(form["yr1"].value)
    except:
        year_end = date.today().year
        pass    
    try:
        month = int(form["mo"].value)
    except:
        month = 0  # i.e. default is all months
        pass
    try:
        callback = form["callback"].value
    except:
        callback = None
        pass
        

    dataset = open_url(config['url'])
    varname = config['var']

    if month != 0:
        month_start = month
        skip = 12
    else:
        month_start = 1
        skip = 1
        pass

    firstday = datetime(year_start,month_start,1, tzinfo=UTC())
    lastday = datetime(year_end,12,31, tzinfo=UTC())
    first = to_udunits(firstday, dataset.time.units)
    last =  to_udunits(lastday, dataset.time.units)
    interval = ((first <= dataset.time) & (dataset.time <= last))

    rainrecs = []
    a = dataset[varname][interval,y,x]
    seq = a.array[::skip]
    times = a.time[::skip]
    



    missing =  dataset[varname].missing_value
    data = numpy.select([seq == missing],[None], default = seq)
    data = (data * dataset[varname].scale_factor + dataset[varname].add_offset)
    values = config['convert'](data)


    plot = []
    i = 0
    for t in times:
        plot.append([udDate(t,dataset),values[i]])
        i += 1
        pass

    report = {}
    report['attributes'] = dataset.attributes
    report['data-url'] = config['url']
    report['data-en'] = config['en']
    report['data'] = plot
    returnJson(report,callback)
    return

if __name__ == '__main__':
  main()
