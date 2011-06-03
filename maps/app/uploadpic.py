#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext.webapp import blobstore_handlers
import os
import urllib
from mappic import MapPic


# Do a get /picuploadurl and the blobstore url is returned.
# See upload.py for more info if that doesn't make sense.
class PicUploadUrlHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/picupload')
        self.response.out.write(upload_url)

class PicUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        year = int(self.request.get('year'))
        month = int(self.request.get('month'))
        dek = int(self.request.get('dek'))
        param = self.request.get('param')
        upload_files = self.get_uploads('pic')
        blob_info = upload_files[0]
        d = MapPic(year=year,month=month,dek=dek,param=param,pic=blob_info.key())
        d.put()
        self.redirect('/done')


