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
from dekadtile import DekadTile

# This form could be used to manually upload data to the datastore and blobstore.
# To upload using curl call UploadUrlHandler instead. 
class FormHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write('<html><body>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""
X: <input type="text" name="x"><br>
Y: <input type="text" name="y"><br>
Year: <input type="text" name="year"><br>
Upload File: <input type="file" name="data"><br> 
Upload File: <input type="file" name="dmin"><br> 
Upload File: <input type="file" name="dmax"><br> 
<input type="submit" name="submit" value="Submit"> </form></body></html>
""")

# A get on this url (probably /uploadurl) will return a blobstore url to which the data should be posted.
# From a bash script something like this is needed -
# url=`curl -s http://wepoco-map.appspot.com/uploadurl`
# curl -F x=$x -F y=$y -F year=$year -F data=@$datfile -F dmin=@$minfile -F dmax=@$maxfile $url
#
class UploadUrlHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write(upload_url)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        x = int(self.request.get('x'))
        y = int(self.request.get('y'))
        year = int(self.request.get('year'))
        upload_files = self.get_uploads('data')  # 'data' is file upload field in the form
        blob_info = upload_files[0]
        upload_files_min = self.get_uploads('dmin') 
        blob_info_min = upload_files_min[0]
        upload_files_max = self.get_uploads('dmax') 
        blob_info_max = upload_files_max[0]
        d = DekadTile(x=x,y=y,year=year,data=blob_info.key(),dmin=blob_info_min.key(),dmax=blob_info_max.key())
        d.put()
        self.redirect('/done')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.response.out.write('<html><body>')
        self.response.out.write('<p>%s</p></body></html>' %  blob_info.key())

