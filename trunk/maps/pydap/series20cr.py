#!/usr/bin/env python
# Michael Saunby.  August 2011.
#
# Purpose:
# Fetch rainfall time series for single grid box. 
#


from pydap.client import open_url
from datetime import datetime, tzinfo, timedelta
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

year_start = 1961
year_end = 2008
# Monthly means are assigned to first day of month. That's why the
# range ends on 1st December.

#dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets20thC_ReanV2/" 
#monthly_monolevel = dods + "Monthlies/gaussian/monolevel/"
#precip_rate_url = dods + "gaussian/monolevel/prate.2008.nc"
#precip_month_url = dods + "Monthlies/gaussian/monolevel/prate.mon.mean.nc"

def udDate(time, dataset):
    date = from_udunits(time, dataset.time.units.replace('GMT', '+0:00'))
    return '%d/%02d/%02d' % (date.year, date.month, date.day)

def code(n):
    if n < 10:
        return chr(ord('0')+n)
    else:
        return chr(ord('A')+n-10)
    pass

def location_str(data, y, x):
    lng =  data.lon[x]
    if lng > 180:
        lng = lng - 360
        pass
    return '%f,%f' % (data.lat[y], lng)

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
        callback = form["callback"].value
    except:
        callback = None
        pass
        
    dataset = open_url(config['url'])
    varname = config['var']
    missing = 32766 # Missing value indicator

    firstday = datetime(year_start,1,1, tzinfo=UTC())
    lastday = datetime(year_end,12,1, tzinfo=UTC())
    first = to_udunits(firstday, dataset.time.units)
    last =  to_udunits(lastday, dataset.time.units)
    interval = ((first <= dataset.time) & (dataset.time <= last))

    rainrecs = []
    a = dataset[varname][interval,y,x]
    seq = a.array[:]
    times = a.time[:]
    

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
    report['data'] = plot
    returnJson(report,callback)
    return

if __name__ == '__main__':
  main()