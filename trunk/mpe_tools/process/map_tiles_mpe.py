#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#
# The last MPE (grib) file of the day will trigger the creation of a PNG
# image.
# For each of the reporojection LUT files in lutdir this
# script will generate a map tile for use with Google Maps.
##############################################################################  

import sys, array, Image

force = False
msatwidth = 2300; msatheight = 2300
msgwidth = 3712; msgheight = 3712

#lut_suffix = '.msat_lut'
lut_suffix = '.msg_lut'
tile_suffix = '.png'
mapconfig = 'map.list'


# Take an image in Meteosat projection, an appropriate reproj LUT and
# generate a new image tile.
def reproj( inpic, lutf, destImgName ):
    outcols = 256
    outrows = 256
    (inrows,incols) = inpic.size
    if incols == msgwidth:
        proj = "msg"
    elif incols == msatwidth:
        # "trimmed" meteosat
        proj = "msat"
        return (1, 'source image old (M7) size')
    else:
        return (1, 'source image wrong size for reproj')

    matrix = array.array('h')
    matrix.fromfile( lutf, outrows*outcols*2 )
    
    outpic = Image.new(inpic.mode,(outcols,outrows))
    for y in range(outrows):
        for x in range(outcols):
            xmsat = matrix[y*outcols*2 + x*2]
            ymsat = matrix[y*outcols*2 + x*2 +1]
            #if incols == msatwidth:
            #    xmsat = xmsat - 100
            #    ymsat = ymsat - 100
            #    pass
            try:
                p = inpic.getpixel((xmsat,ymsat))
                outpic.putpixel((x,y), p)
            except:
                pass
            pass
        pass

    outpic.putpalette( inpic.getpalette() )
    outpic.save( destImgName, transparency=0 )

    return (0, '')

import os, string

from fn_mk_tiledir import mk_tiledir

def run( workdir = '/home/mike/wepoco/data/mpe/', sumname=None ):
    bindir='/home/mike/wepoco/bin/'
    datadir='/home/mike/wepoco/data/mpe/'
    #mapdir=datadir + 'map/'
    lutdir=datadir + 'lut/'
    config = 'acc.out'

    if not sumname:
        try:
            configf = file( workdir + config, 'r' )
            discard = string.strip( configf.readline() )
            sumname = string.strip( configf.readline() )
            lasttmp = string.strip( configf.readline() )
            configf.close()
        except Exception, inst:
            # print inst
            return (1, 'Failed to read configuration file')

        if (lasttmp == 'last'):
            islast = True
        else:
            return (2, 'Not last file of day')
        pass

    try:
        imgname = sumname + '.png'
        tiledir = mk_tiledir( workdir, sumname )

        # Open sum image file.
        satimg = Image.open( workdir + imgname )
    except:
        return (3, 'Failed to open input image file %s' % (workdir + imgname))

    #

    # Create new images
    try:
        lutconf = file( lutdir + mapconfig, 'r' )
    except:
        return (4, 'Failed to open map config file' )
    if True:
        for mapname in lutconf:
            mapname = string.strip( mapname )
            words = string.split( mapname, '.' )
            lutname = words[0] + lut_suffix
            tilename = words[0] + tile_suffix
            try:
                if force:
                    print "processing", tilename
                    pass
                lutf = file( lutdir + lutname, 'rb' )
                (rc, msg) = reproj( satimg, lutf, workdir + tiledir + tilename )
                if rc:
                    print msg
                    pass
            except Exception, inst:
                print inst
                return (5, 'Failed when processing %s' % (lutname))
            pass
        pass
    
    return (0, 'OK')

if __name__ == "__main__":
    import sys
    force = True
    (rc, msg) = run( './', sumname=sys.argv[1] )
    print msg
    sys.exit( rc )


