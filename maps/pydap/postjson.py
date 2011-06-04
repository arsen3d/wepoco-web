#!/usr/bin/python

import urllib, urllib2
import json
import sys


# define a Python data dictionary
#data = {'first_name': 'Devin', 'last_name': 'Fee', 'url': 'http://devinfee.com/blog'}
#data_json = json.dumps(data)

obj = json.load(file(sys.argv[1],'rb'))

#data_json = json.dumps(obj)

data_json = urllib.urlencode({'jsonData' : json.dumps(obj)})

host = "http://localhost:8080/uploadrean"
req = urllib2.Request(host, data_json)#, {'content-type': 'application/json'})
response_stream = urllib2.urlopen(req)
response = response_stream.read()
print response
