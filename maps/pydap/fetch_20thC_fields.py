#!/usr/bin/python
#
#
# Design aims:
#
# Download chosen data for specified date range and lat/long region.
# Output as csv suitable for upload to Fusion Tables
# Or export directly to Fusion Tables using api
# Or upload to AppEngine
# 
# Consider how "merge" might be used to extend output tables to more parameters
# Consider extracting multiple parameters and combining in single output CSV.
# Use time_bnds and give start and end date


from pydap.client import open_url
#from dap.client import open as open_url
from datetime import datetime, tzinfo, timedelta
from coards import from_udunits, to_udunits
import numpy
import csv
import sys

class UTC(tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return "UTC" 
    def dst(self, dt):
        return timedelta(0)
    pass

year = int(sys.argv[1])

# A list of (lat,lon) coordinate pairs, each defines
# a rectangle.  Together they form an approximation of the
# continent of Africa.
regions = [[(38.0,-17.0),(3.0,0.0)],
           [(38.0,0.0),(3.0,13.0)],
           [(33,13),(3,38)],
           [(22,38),(3,52)],
           [(3,8),(-26,52)],
           [(-26,14),(-36,34)]] 

first = datetime(year,1,1, tzinfo=UTC())
last = datetime(year,12,1, tzinfo=UTC())

dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/" 
monthly_monolevel = dods + "20thC_ReanV2/Monthlies/gaussian/monolevel/"
air_sfc_mon_mean_url = monthly_monolevel + "air.sfc.mon.mean.nc"
air_2m_mon_mean_url = monthly_monolevel + "air.2m.mon.mean.nc"

dataset = open_url(air_2m_mon_mean_url)
print dataset.keys()

first = to_udunits(first, dataset.time.units)
last =  to_udunits(last, dataset.time.units)
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

outfile = "africa_2m_temp_%d.csv" % year
csvout = csv.writer(open(outfile,'wb'))
csvout.writerow(["date","locn_id","location","celsius"])

nregions = len(regions)
  
for r in range(nregions):
    (n,w) = regions[r][0]
    (s,e) = regions[r][1]
    w = w%360
    e = e%360
    if e == 0: e=360
    print "nw", n,w, "se", s,e
    a = dataset.air[interval,
                    (dataset.lat > s) & (dataset.lat < n),
                    (dataset.lon >= w) & (dataset.lon < e) ]
    #print "shape", a.shape
    data = numpy.round(a.array[:] * dataset.air.scale_factor + dataset.air.add_offset - 273.15, 1)
    #print "data shape", data.shape
    (ntimes, nlats, nlons) = data.shape

    for t in range(ntimes):
        print from_udunits(a.time[t], dataset.time.units.replace('GMT', '+0:00'))
        for la in range(nlats):
            for lo in range(nlons):
                loc_code = code(r) + code(la) + code(lo)
                csvout.writerow([date_str(a.time[t]),loc_code,
                                 location_str(a, la, lo),
                                 data[t,la,lo]])





