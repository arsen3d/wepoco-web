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


def region_select(nwcorner, secorner):
    (nlat,wlon) = nwcorner
    (slat,elon) = secorner
    wlon = wlon % 360
    elon = elon % 360
    print "lon range", wlon, elon
    if wlon > elon:
        print "split lon a,-1 0,b"
    else:
        pass
    if slat > nlat:
        print "split lat"
    else:
        pass
    
    return

def time_range(timebnds, first, last):
    tidx = 0
    included = []
    for t in timebnds:
        # replace t[0] with t is using 'time' rather than 'time_bnds'
        date = from_udunits(t[0], dataset.time.units.replace('GMT', '+0:00'))
        if (date >= first) & (date <= last):
            print "include", tidx, t, date
            included.append(tidx) 
            pass
        tidx += 1
        pass
    print "RANGE", included[0], included[-1] 
    return

dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/" 
monthly_monolevel = dods + "20thC_ReanV2/Monthlies/gaussian/monolevel/"
air_sfc_mon_mean_url = monthly_monolevel + "air.sfc.mon.mean.nc"
air_2m_mon_mean_url = monthly_monolevel + "air.2m.mon.mean.nc"



dataset = open_url(air_2m_mon_mean_url)
print dataset.keys()

air = dataset['air']
time = dataset['time']

if 0:
    print type(air)
    print air.dimensions
    print air.shape
    print air.attributes    
    pass

grid = air.array[1655,0:93:10,0:191:10] * air.scale_factor + air.add_offset - 273.17
grid = numpy.round(grid,1)
print grid.shape
print dataset['time_bnds'].shape

for t in dataset['time_bnds'][1655]:
    date = from_udunits(t, dataset.time.units.replace('GMT', '+0:00'))
    print date

ZERO = timedelta(0)
class UTC(tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

first = datetime(2005,1,1, tzinfo=UTC())
last = datetime(2005,2,1, tzinfo=UTC())

#time_range(dataset.time_bnds, first, last)
#region_select((40.1,-50.2),(-50.3,45.4))

first = to_udunits(first, dataset.time.units)
last =  to_udunits(last, dataset.time.units)

#print dataset.time_bnds[ (first <= dataset.time) & (dataset.time <= last)]
print dataset.time_bnds[(first==dataset.time) | (last==dataset.time)]
#print dataset.air[(first==dataset.time),0:93:10,0:191:10]
#interval = (first==dataset.time)
interval = ((first<=dataset.time) & (dataset.time <= last))
a = dataset.air[interval,0:93:10,(dataset.lon > 350) & (dataset.lon < 360) ]
#b = dataset.air[interval,0:93:10,(dataset.lon >= 0) & (dataset.lon < 10) ]

print air.attributes
print air.time[:]
print air.lat[:]
print air.lon[:]




# For a single date use axis=1
#c = numpy.concatenate((a, b), axis=2)
#c = numpy.round(c * air.scale_factor + air.add_offset - 273.17, 1)
#print c
#print dataset.lon[0:-1]




