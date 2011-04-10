#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.ext import blobstore
from google.appengine.ext import db

class DekadTile(db.Model):
    y = db.IntegerProperty(required=True)
    x = db.IntegerProperty(required=True)
    year = db.IntegerProperty(required=True)
    data = blobstore.BlobReferenceProperty()
    dmin = blobstore.BlobReferenceProperty()
    dmax = blobstore.BlobReferenceProperty()
    pass

