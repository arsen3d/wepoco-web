#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext import db
from dekadtile import DekadTile
from array import array
# Using simplejson as json library not available in App Engine 
# - they're equivalent.
from django.utils import simplejson

#
# HTTP GET with query ....
# return is json text or jsonp if callback=somefnname
#

## Could search for orphans with something like - 
#blobs = BlobInfo.all().fetch(500)
#for blob in blobs:
#  if not MyModel.all().filter("blob_ref =", blob.key()).count(1):
#    blob.delete()

class ListBlobs(webapp.RequestHandler):
    def get(self):
        self.getArgs()
        self.list = []
        self.labels = ['filename','creation','key']
        query = blobstore.BlobInfo.all()
        for b in query:
            self.list.append([b.filename,str(b.creation),str(b.key())])
            pass
        self.returnJson()
        return
    
    def getArgs(self):
        self.callback = self.request.get("callback")
        return

    def returnJson(self):
        self.response.headers['Content-type'] = 'text/json'
        resp = {}
        resp['data'] = self.list
        resp['labels'] = self.labels
        if self.callback:
            self.response.out.write("%s(" % self.callback)
            pass
        self.response.out.write(simplejson.dumps(resp))
        if self.callback:
            self.response.out.write(");")
            pass
        return

class DelBlobs(webapp.RequestHandler):
    def post(self):
        req = simplejson.loads(self.request.body)
        dellist = []
        for r in req:
            dellist.append(r['key'])
            pass
        blobstore.delete(dellist)
        self.response.out.write(simplejson.dumps(dellist))
        return
    

