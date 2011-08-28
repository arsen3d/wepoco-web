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
import sys
import cgi

class UTC(tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return "UTC" 
    def dst(self, dt):
        return timedelta(0)
    pass

year_start = 1900
year_end = 2008
# Monthly means are assigned to first day of month. That's why the
# range ends on 1st December.
firstday = datetime(year_start,1,1, tzinfo=UTC())
lastday = datetime(year_end,12,1, tzinfo=UTC())

dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets20thC_ReanV2/" 
monthly_monolevel = dods + "Monthlies/gaussian/monolevel/"

precip_rate_url = dods + "gaussian/monolevel/prate.2008.nc"
precip_month_url = dods + "Monthlies/gaussian/monolevel/prate.mon.mean.nc"
dataset = open_url(precip_month_url)
varname = "prate"
missing = 32766 # Missing value indicator
secs_per_month = 2592000 # Assume all months 30 days

#alllats = dataset.lat[:]
#alllons = dataset.lon[:]

first = to_udunits(firstday, dataset.time.units)
last =  to_udunits(lastday, dataset.time.units)
interval = ((first <= dataset.time) & (dataset.time <= last))


def date_str(time):
    date = from_udunits(time, dataset.time.units.replace('GMT', '+0:00'))
    return '%d-%02d-%02d' % (date.year, date.month, date.day)


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

def main():
    form=cgi.FieldStorage()
    x = int(form["x"].value)
    y = int(form["y"].value)
    rainrecs = []
    a = dataset[varname][interval,y,x]
    seq = a.array[:]
    data = numpy.select([seq == missing],[None], default = seq)
    data = (data * dataset[varname].scale_factor + dataset[varname].add_offset)
    data *= secs_per_month
    ntimes = data.shape

    rain = data[:].astype('int')
    b = {}
    b['first'] = firstday.strftime("%Y/%m/%d")
    b['last'] = lastday.strftime("%Y/%m/%d")
    b['rain'] = rain.tolist()
    rainrecs.append(b)

    report={}
    report['rainrecs'] = rainrecs
    print "Content-type: text/json\n"
    print json.dumps(report)


if __name__ == '__main__':
  main()
