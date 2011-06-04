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
import json
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

#year = int(sys.argv[1])

# A list of (lat,lon) coordinate pairs, each defines
# a rectangle.  Together they form an approximation of the
# continent of Africa.
regions = [[(38.0,-17.0),(3.0,0.0)],
           [(38.0,0.0),(3.0,13.0)],
           [(33,13),(3,38)],
           [(22,38),(3,52)],
           [(3,8),(-26,52)],
           [(-26,14),(-36,34)]] 

#regions = [[(-26,14),(-36,34)]] 

year = 2000
year_start = 2000
year_end = 2008
firstday = datetime(year_start,1,1, tzinfo=UTC())
lastday = datetime(year_end,12,1, tzinfo=UTC())

dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets20thC_ReanV2/" 
monthly_monolevel = dods + "Monthlies/gaussian/monolevel/"
air_sfc_mon_mean_url = monthly_monolevel + "air.sfc.mon.mean.nc"
air_2m_mon_mean_url = monthly_monolevel + "air.2m.mon.mean.nc"

precip_rate_url = dods + "gaussian/monolevel/prate.2008.nc"
precip_month_url = dods + "Monthlies/gaussian/monolevel/prate.mon.mean.nc"
#dataset = open_url(air_2m_mon_mean_url)
dataset = open_url(precip_month_url)
varname = "prate"
missing = 32766
secs_per_month = 2592000

print dataset.keys()

alllats = dataset.lat[:]
alllons = dataset.lon[:]

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

outfile = "africa_2m_temp_%d.csv" % year
csvout = csv.writer(open(outfile,'wb'))
csvout.writerow(["date","locn_id","location","celsius"])

nregions = len(regions)

rainrecs = []
for r in range(nregions):
    (n,w) = regions[r][0]
    (s,e) = regions[r][1]
    w = w%360
    e = e%360
    if e == 0: e=360
    print "nw", n,w, "se", s,e
    a = dataset[varname][interval,
                    (dataset.lat > s) & (dataset.lat < n),
                    (dataset.lon >= w) & (dataset.lon < e) ]
    # For temperature in C
    #data = numpy.round(a.array[:] * dataset[varname].scale_factor + 
    #                   dataset[varname].add_offset - 273.15, 1)

    x = a.array[:]
    print a.lat[:]
    print a.lon[:]
    data = numpy.select([x == missing],[None], default = x)
    data = (data * dataset[varname].scale_factor + dataset[varname].add_offset)
    data *= secs_per_month

    #data = data.round()

    (ntimes, nlats, nlons) = data.shape
    print " (ntimes, nlats, nlons) ", ntimes, nlats, nlons
    for la in range(nlats):
        for lo in range(nlons):
            rain = data[:,la,lo].astype('int')
            #csvout.writerow(a)
            b = {}
            b['first'] = firstday.strftime("%Y/%m/%d")
            b['last'] = lastday.strftime("%Y/%m/%d")
            b['laidx'] = int(numpy.where(alllats == a.lat[la])[0])
            b['loidx'] = int(numpy.where(alllons == a.lon[lo])[0])
            b['lat'] = "%.4f" % a.lat[la].astype('float')
            b['lng'] = "%.4f" % a.lon[lo].astype('float')
            b['rain'] = rain.tolist()
            rainrecs.append(b)

#    for t in range(ntimes):
#        print from_udunits(a.time[t], dataset.time.units.replace('GMT', '+0:00'))
#        for la in range(nlats):
#            for lo in range(nlons):
#                loc_code = code(r) + code(la) + code(lo)
#                csvout.writerow([date_str(a.time[t]),loc_code,
#                                 location_str(a, la, lo),
#                                 numpy.round(data[t,la,lo],1)])


report={}
report['rainrecs'] = rainrecs
report['lats'] = alllats.tolist()
report['lons'] = alllons.tolist()

json.dump(report, file('out.json','wb'))


