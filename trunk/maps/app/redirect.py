#!/usr/bin/env python
#
# Copyright 2008 Wepoco.  http://www.wepoco.org/
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
###
# Notes on testing in SDK.
# Delete database if changes in code cause failures.  'rm $TMP/dev_appstore.*'
#
# Notes on deployment.
#
#

import wsgiref.handlers
from google.appengine.ext import webapp
import logging
from urlparse import urlparse

redirects = {}
redirects["www.wepoco.com"] = "http://www.wepoco.org";
redirects["map.wepoco.com"] = "/map";

class myHandler(webapp.RequestHandler):
  def get(self):
    url =  urlparse(self.request.url)
    logging.debug("myHandler redirect from %s", url.netloc)

    try:
      r = redirects[url.netloc]
      logging.debug("myHandler redirect to %s", r)
      #self.response.out.write("Called as [" + url.netloc + "]")
      #self.response.out.write("  Redirecting to " + r)
      self.redirect( r )
    except:
      self.response.out.write("Called as [" + url.netloc + "]")
      pass
#    try:
#      # redirect
#    except Error:
#      # Clear output and return an error code.
#      self.error(500)
#
    return
  pass

application = webapp.WSGIApplication([
  ('.*', myHandler)
], debug=True)

def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
