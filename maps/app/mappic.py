#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.ext import blobstore
from google.appengine.ext import db

class MapPic(db.Model):
    param =  db.StringProperty()
    year = db.IntegerProperty(required=True)
    month = db.IntegerProperty(required=True)
    dek = db.IntegerProperty(required=True)
    pic = blobstore.BlobReferenceProperty()
    pass

