#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $$
#

#
# Configuration
#

import sys, httplib
import Image, ImageDraw
import cStringIO
import cgi
#import cgitb; cgitb.enable()

site = 'wepoco.s3.amazonaws.com'
prefix = '/'

ref_zoom = 5
outcols = 256
outrows = 256

contenttype = "image/png"

def getArgs():
    global x, y, z, mapname, typename
    form = cgi.FieldStorage()
    try:
        x = int(form["x"].value)
        y = int(form["y"].value)
        z = int(form["zoom"].value)
        mapname = form["map"].value
        typename = form["type"].value
    except:
        pass



def download( url_fname ):
    conn = httplib.HTTPConnection( site )
    conn.request( 'GET', url_fname )
    r1 = conn.getresponse()
    if r1.status == 200:
	f = cStringIO.StringIO()
	f.write(r1.read())
	f.seek(0)
	return f
    else:
	return None


def zoom():
    tile_x = x / (2** (z - ref_zoom))
    tile_y = y / (2** (z - ref_zoom))
    imgname = "%s/%s/%d/%d_%d.png" % (typename,mapname,ref_zoom,tile_x,tile_y)
    try:
        imgstream = download( prefix + imgname ) 
        inpic = Image.open( imgstream )
        (inrows,incols) = inpic.size
        width = height = 256 / (2** (z - ref_zoom))
        xoffset = width * (x % (2** (z - ref_zoom)))
        yoffset = height * (y % (2** (z - ref_zoom)))
        box =  (xoffset, yoffset, xoffset + width, yoffset + height )
        outpic = inpic.crop( box )
        outpic = outpic.resize( (outcols,outrows) )
        f = cStringIO.StringIO()
        outpic.save(f, "PNG", transparency=0)
    except:
        f = file(no_data)
        pass
    print "Content-type: image/png\n"
    f.seek(0)
    print f.read()
    f.close()
    return

if __name__ == "__main__":
    getArgs()
    zoom()
