#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.ext import blobstore
from google.appengine.ext import db

class RfePic(db.Model):
    year = db.IntegerProperty(required=True)
    month = db.IntegerProperty(required=True)
    dek = db.IntegerProperty(required=True)
    pic = blobstore.BlobReferenceProperty()
    pass

