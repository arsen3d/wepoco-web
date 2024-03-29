#!/usr/bin/env python
#
# Copyright 2011 Wepoco.  http://www.wepoco.org/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###
# Notes on testing in SDK.
# Delete database if changes in code cause failures.  'rm $TMP/dev_appstore.*'
# or use -c  (clear option) on dev_appserver.py command line
# also http://localhost:8080/_ah/admin can delete, etc.
#
#

import wsgiref.handlers
from google.appengine.ext import webapp
from adminlistblobs import ListBlobs, DelBlobs
from adata import AData
from arfe import ARfe, ANdvi
from arean import ARean
from astation import AStnRain
from arfeimg import ARfeImg, ANdviImg
from upload import *
from uploadpic import *
from uploadrean import *
from uploadstnrain import *
from getcsv import *
from getmetdata import *

application = webapp.WSGIApplication([  
  ('/listblobs', ListBlobs),
  ('/delblobs', DelBlobs),
  ('/adata', AData),
  ('/arfe', ARfe),
  ('/arean', ARean),
  ('/astnrain', AStnRain),
  ('/andvi', ANdvi),
  ('/arfeimg', ARfeImg),
  ('/andviimg', ANdviImg),
  ('/upload', UploadHandler),
  ('/uploadform', FormHandler),
  ('/uploadurl', UploadUrlHandler),
  ('/uploadrean', UploadReanHandler),
  ('/uploadstnrain', UploadStnRainHandler),
  ('/picuploadurl', PicUploadUrlHandler),
  ('/picupload', PicUploadHandler),
  ('/getcsv', GetCSV),
  ('/getmetdata', GetMetData),
  ('/serve/([^/]+)?', ServeHandler),
], debug=True)

def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
