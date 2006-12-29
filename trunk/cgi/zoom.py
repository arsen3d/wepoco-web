#!/usr/bin/python
#
# zoom.py
# Michael Saunby. 3rd December 2006.  For Wepoco.
#
# Allow user to view Google Map format tiles
# at higher than supplied resolutions
# by dynamic scaling and cropping.
#
#
import Image, ImageDraw
import cStringIO
from random import randint as rint
import cgi
import cgitb; cgitb.enable()
import sys

datadir = "/home/wepoco/ftp/mpe"
#datadir = "/home/mike/wepoco/data/mpe"

contenttype = "image/png"
outcols = 256
outrows = 256
ref_zoom = 5
no_data = datadir + "/no_data.png"

# The global vars x,y,z,and mapname are
# replaced by values passed to this cgi script from the calling
# web page.  (well through the Javascript called from Google Maps API).
x = 0
y = 0
z = 0
mapname="MAP_NAME_HERE!!"

def getArgs():
    global x, y, z, mapname
    form = cgi.FieldStorage()
    try:
        x = int(form["x"].value)
        y = int(form["y"].value)
        mapname = form["map"].value
    except:
        pass
    z = int(form["zoom"].value)


def zoom():
    tile_x = x / (2** (z - ref_zoom))
    tile_y = y / (2** (z - ref_zoom))
    imgname = "%s/%s/%d/%d_%d.png" % (datadir,mapname,ref_zoom,tile_x,tile_y)
    try:
        inpic = Image.open( imgname )
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
    if z < 6:
        print "Content-type: image/png\n"
        imgname = "%s/%s/%d/%d_%d.png" % (datadir,mapname,z,x,y)
        try:
            f = file(imgname)
        except:
            f = file(no_data)
            pass
        print f.read()
        f.close()
    else:
        zoom()
        
