#!/usr/bin/env python
# Michael Saunby.  December 2011.
#
# Purpose:
# Fetch time series for single grid box.  This code began its life fetching monthly mean
# values and has beed adapted to get either these, or sub daily data.  In the case of 
# sub daily data yr0 and yr1 must be the same, or adjacent.  Modifying to longer runs
# wouldn't be too hard. 
#

import pydap.lib
pydap.lib.CACHE = "/tmp/pydap-cache/"
from pydap.client import open_url
from datetime import datetime, tzinfo, timedelta, date
from coards import from_udunits, to_udunits
import numpy
#import csv
#import json
#from json import encoder
#encoder.FLOAT_REPR = lambda o: format(o, '.1f')
import sys
import cgi
# gviz_api.py available here http://code.google.com/p/google-visualization-python/
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
    month_start = 0
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
        month_start = int(form["mo"].value)
    except:
        pass
    try:
        month_start = int(form["mo0"].value)
    except:
        pass
    try:
        month_end = int(form["mo1"].value)
    except:
        month_end = 12
        pass
    try:
        q = form["q"].value
        config = months20cr[q]
        if month_start == 0:
            month_start = 1
            skip = 1
        else:
            skip = 12
            pass
    except:
        try:
            fi = form["fi"].value
            config = {}
            config['url'] = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets20thC_ReanV2/" + \
            "gaussian/monolevel/" + fi + "." + str(year_start) + ".nc"
            config['url2'] = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets20thC_ReanV2/" + \
            "gaussian/monolevel/" + fi + "." + str(year_end) + ".nc"
            config['var'] = fi.split(".")[0]
            config['en'] = fi
            config['convert'] = lambda data: data[:]
            skip = 1
        except:
            k =  months20cr.keys()
            warn("q must be one of " + str(k))
            return
        pass
    
    varname = config['var']

    firstday = datetime(year_start,month_start,1, tzinfo=UTC())
    if (month_end == 12):
        lastday = datetime(year_end,12,31, tzinfo=UTC())
    else:
        lastday = datetime(year_end,month_end+1,1, tzinfo=UTC())
        pass

    outdata = []

    # At present this code has 1 or 2 urls, but the code here could easily be extended 
    # to cope with more, just add them to the list 'urls', but make sure they're in the
    # correct order, oldest data first.
    urls = [config['url']]
    try:
        urls.append(config['url2'])
    except:
        pass

    for dataurl in urls:
        dataset = open_url(dataurl)
        first = to_udunits(firstday, dataset.time.units)
        last =  to_udunits(lastday, dataset.time.units)
        (x,y) = toXY(lat,lng)
        # Note one or other (or both) of the start or end times could be outside the
        # range of a given dataset, that's fine and no problems will result.
        a = dataset[varname][(first <= dataset.time) & (dataset.time <= last),y,x]
        seq = a.array[::skip]
        times = a.time[::skip]
        latitude = dataset['lat'][y]
        longitude =  dataset['lon'][x]
        
        missing =  dataset[varname].missing_value
        data = numpy.select([seq == missing],[None], default = seq)
        data = (data * dataset[varname].scale_factor + dataset[varname].add_offset)
 
        # Get the values and loop over them inserting into the outdata list
        # csv and json require slightly different treatment.
        values = config['convert'](data).astype('float').tolist()
        i = 0
        if tqx['out'] == 'csv':
            for t in times:
                # See comment below.
                outdata.append({"date":str(dDate(t,dataset)),"value":values[i]})
                i += 1
                pass
            pass
        else:
            for t in times:
                outdata.append({"date":dDate(t,dataset),"value":values[i]})
                i += 1
                pass
            pass
        pass

# Loading it into gviz_api.DataTable
# Default output is 'json'.  Ideally this is specified as tqx=out:json
# but even when it isn't, that's what is produced.
# For CSV the date and time is presented as a string, otherwise it would be a
# javascript "new Date()" object.  


    if tqx['out'] == 'csv':
        description = {"date": ("string", "Date"),
                       "value": ("number", config['en'])}
    else:
        description = {"date": ("datetime", "Date"),
                       "value": ("number", config['en'])}
        pass

    data_table = gviz_api.DataTable(description)
    data_table.LoadData(outdata)

    if tqx['out'] == 'csv':
        print 'Content-type: text/plain\n'
        csv = data_table.ToCsv(columns_order=("date", "value"),order_by="date",separator=",")
        print csv
    else:
        json = data_table.ToJSonResponse(columns_order=("date", "value"), order_by="date", 
                                         req_id=tqx['reqId'])
        print 'Content-type: text/plain\n'
        print json
        pass
    return
    

if __name__ == '__main__':
  main()
