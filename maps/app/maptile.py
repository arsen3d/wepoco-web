#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

from google.appengine.api import urlfetch, images
from google.appengine.ext import webapp
from xml.etree.ElementTree import Element, SubElement, ElementTree, fromstring

class MapTile(db.Model):
    name = db.StringProperty()
    png = db.BlobProperty()


