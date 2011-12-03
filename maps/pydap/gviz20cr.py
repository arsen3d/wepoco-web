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
import gviz_api
from coords20cr import toXY

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

def dDate(time, dataset):
    date = from_udunits(time, dataset.time.units.replace('GMT', '+0:00'))
    return date

def warn(msg):
    print 'Content-type: text/plain\n'
    print msg

def main():
    form=cgi.FieldStorage()
    tqx={}
    tqx['reqId']=0
    tqx['out']='json'
    try:
        tqxa=form["tqx"].value
        tqxa=tqxa.split(';')
        for kv in tqxa:
          (k,v)=kv.split(':')
          tqx[k]=v
          pass
    except:
        pass
    try:
        lat = float(form["lat"].value)
        lng = float(form["lng"].value)
    except:
        warn("lat and lng must be floats.")
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
        q = form["q"].value
        config = months20cr[q]
        if month != 0:
            month_start = month
            skip = 12
        else:
            month_start = 1
            skip = 1
            pass
    except:
        try:
            fi = form["fi"].value
            config = {}
            config['url'] = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets20thC_ReanV2/" + \
            "gaussian/monolevel/" + fi + "." + str(year_start) + ".nc"
            config['var'] = fi.split(".")[0]
            config['en'] = fi
            config['convert'] = lambda data: data[:]
            month_start = 1
            skip = 8
        except:
            k =  months20cr.keys()
            warn("q must be one of " + str(k))
            return
        pass
    

    dataset = open_url(config['url'])
    varname = config['var']


    firstday = datetime(year_start,month_start,1, tzinfo=UTC())
    lastday = datetime(year_end,12,31, tzinfo=UTC())
    first = to_udunits(firstday, dataset.time.units)
    last =  to_udunits(lastday, dataset.time.units)
    interval = ((first <= dataset.time) & (dataset.time <= last))

    rainrecs = []
    (x,y) = toXY(lat,lng)
    a = dataset[varname][interval,y,x]
    seq = a.array[::skip]
    times = a.time[::skip]
    #latitude = a.lat
    #longitude = a.lon
    latitude = dataset['lat'][y]
    longitude =  dataset['lon'][x]

    missing =  dataset[varname].missing_value
    data = numpy.select([seq == missing],[None], default = seq)
    data = (data * dataset[varname].scale_factor + dataset[varname].add_offset)
    values = config['convert'](data).astype('float').tolist()

    data = []
    i = 0
    for t in times:
        data.append({"date":dDate(t,dataset),"value":values[i]})
        i += 1
        pass

    description = {"date": ("date", "Date"),
                   "value": ("number", config['en'])}
    
  # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    if tqx['out'] == 'json':
        # Creating a JSon string
        json = data_table.ToJSonResponse(columns_order=("date", "value"), order_by="date", 
                                         req_id=tqx['reqId'])
        print 'Content-type: text/plain\n'
        print json
    elif tqx['out'] == 'csv':
        print 'Content-type: text/plain\n'
        csv = data_table.ToCsv(columns_order=("date", "value"), order_by="date",
                                       separator=", ")
        print csv
        pass
    return
    

if __name__ == '__main__':
  main()
