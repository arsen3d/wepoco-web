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


"""
Could try reading directory, eg.
"http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/20thC_ReanV2/catalog.xml"
"""

from pydap.client import open_url
import sys
from datetime import datetime, tzinfo, timedelta 
from coards import from_udunits, to_udunits
import numpy

dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/" 
#monthly = dods + "20thC_ReanV2/Monthlies/"

#monthly_monolevel = dods + "20thC_ReanV2/Monthlies/gaussian/monolevel/"
#air_sfc_mon_mean_url = monthly_monolevel + "air.sfc.mon.mean.nc"
#air_2m_mon_mean_url = monthly_monolevel + "air.2m.mon.mean.nc"

dods = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/"

#try this "20thC_ReanV2/Monthlies/gaussian/monolevel/air.2m.mon.mean.nc"
# or this "ncep.reanalysis.derived/surface_gauss/prate.sfc.mon.mean.nc"

dataset = open_url(dods + sys.argv[1])
print dataset.keys()

time = dataset['time']

if len(sys.argv)>2:
    param = dataset[sys.argv[2]] 
    print type(param)
    print param.dimensions
    print param.shape
    print param.attributes    
    #print param.time[:]
    #print param.lat[:]
    #print param.lon[:]
    pass





