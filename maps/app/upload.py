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

class DekadTile(db.Model):
    y = db.IntegerProperty(required=True)
    x = db.IntegerProperty(required=True)
    year = db.IntegerProperty(required=True)
    data = blobstore.BlobReferenceProperty(required=True)
    pass

class FormHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""
X: <input type="text" name="x"><br>
Y: <input type="text" name="y"><br>
Year: <input type="text" name="year"><br>
Upload File: <input type="file" name="file"><br> 
<input type="submit" name="submit" value="Submit"> </form></body></html>
""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        x = int(self.request.get('x'))
        y = int(self.request.get('y'))
        year = int(self.request.get('year'))
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        d = DekadTile(x=x,y=y,year=year,data=blob_info.key())
        d.put()
        self.redirect('/done')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.response.out.write('<html><body>')
        self.response.out.write('<p>%s</p></body></html>' %  blob_info.key())
        #self.send_blob(blob_info)
