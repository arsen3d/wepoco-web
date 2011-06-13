#!/usr/bin/python

import urllib, urllib2
import json
import sys



obj = json.load(file(sys.argv[1],'rb'))

#rstart = 0
#rend = 20

rstart = 440
rend = 460

while rstart < len(obj['rainrecs']): 
    print rstart
    a = obj['rainrecs'][rstart:rend]
    rstart += 20
    rend += 20
    uploaddata={}
    uploaddata['lats']=obj['lats']
    uploaddata['lons']=obj['lons']
    uploaddata['rainrecs']=a
    data_json = urllib.urlencode({'jsonData' : json.dumps(uploaddata)})
    #host = "http://localhost:8080/uploadrean"
    host = "http://map.wepoco.com/uploadrean"
    req = urllib2.Request(host, data_json)
    response_stream = urllib2.urlopen(req)
    response = response_stream.read()
    #print response
    pass

