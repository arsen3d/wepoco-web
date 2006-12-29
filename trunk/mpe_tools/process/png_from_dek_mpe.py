#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#
# This script should be called by cron after each new mpe grib file
# has been downloaded.  It will deliberately fail except for the last
# file of the day.

##############################################################################  

import sys, array, Image

backgroundColour = (190, 190, 190) # red, green, blue components
msg_width = 3712
msg_height = 3712

force = False

#
# TAMSAT colour scale
#  mm  Red Green Blue
#   1  100     0  100
#  10  255     0    0
#  20  255   128    0
#  30  255   255    0
#  60    0   255    0
#  90    0   128    0
# 120    0    64    0
# 150    0     0  255
# 200    0     0  128
# 250    0    64  128

def set_palette( img ):
    palette = array.array('h')
    # First entry is set to black, but will later treat as transparent.
    (r,g,b) = backgroundColour
    palette.append(r)
    palette.append(g)
    palette.append(b)
    for entry in range(1, 10):
        (r,g,b) = (100,0,100)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    for entry in range(10, 20):
        (r,g,b) = (255,0,0)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    for entry in range(20, 30):
        (r,g,b) = (255,128,0)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    for entry in range(30, 60):
        (r,g,b) = (255,255,0)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    for entry in range(60, 90):
        (r,g,b) = (0,255,0)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    for entry in range(90, 120):
        (r,g,b) = (0,128,0)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    for entry in range(120, 150):
        (r,g,b) = (0,64,0)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    for entry in range(150, 200):
        (r,g,b) = (0,0,255)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    for entry in range(200, 250):
        (r,g,b) = (0,0,128)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    for entry in range(250, 256):
        (r,g,b) = (0,64,128)
        palette.append(int(r)); palette.append(int(g)); palette.append(int(b))
        pass
    #
    #for entry in range(255):
    #    palette.append( 254-entry )
    #    palette.append( 0 )
    #    palette.append( entry )
    #    pass
    img.putpalette( palette )
    return


def scale_png( scale_name ):
    import ImageDraw
    width = 256
    height = 20
    # Create new image
    img = Image.new( 'P', (width,height) )
    set_palette( img )
    draw = ImageDraw.Draw( img )
    for x in range(width):
        draw.line((x,0) + (x,height), fill=x)
        pass
    img.save( scale_name, transparency=0 )    
    return
    
    
def data_png( infile, outimg, logfile ):

    # Note these files are based on standard Meteosat projection
    # with true width and height of 2500 but with 100 pixels cropped
    # from each edge of the image.
    #
    # width = 2300
    # height = 2300
    width = msg_width
    height = msg_height

    data = array.array( 'd' )
    data.fromfile( infile, width*height )


    scale = 500.0

    imgdat = array.array('B')

    minfound = 10000.0
    maxfound = 0.0
    
    for x in data:
        if x == 9999.0:
            x = 0.0
            pass
        elif x > maxfound:
            maxfound = x
            pass
        elif x < minfound:
            minfound = x
            pass
        try:
            x = x  * scale
            imgdat.append( int(x) )
        # OverflowError
        except:
            imgdat.append( 255 )
        pass

    del(data)
    set_palette( outimg )
    outimg.putdata( imgdat )
    del(imgdat)

    return


import os, string

def run( datadir ='/home/mike/wepoco/data/mpe/', dek_filename = None ):
    bindir='/home/mike/wepoco/bin/'
    config = 'acc.out'

    try:
        # Open dek file.
        dekfile = file( datadir + dek_filename, 'rb' )
    except:
        return (3, 'Failed to open dek file')

    scale_png( datadir + "dek_scale.png" )
    
    # Create new image
    img = Image.new( 'P', (msg_width, msg_height) )
    logf = file( '/tmp/png_from__dek_mpe.log', 'w' )
    rc = data_png( dekfile, img, logf )
    img = img.rotate( 180 )
    imgname = dek_filename + '.png'
    img.save( datadir + imgname, transparency=0 )

    return (0, 'OK')

if __name__ == "__main__":
    import sys
    force = True
    print '# generating PNG for', sys.argv[1]
    (rc, msg) = run('./', sys.argv[1])
    print msg
    sys.exit( rc )


