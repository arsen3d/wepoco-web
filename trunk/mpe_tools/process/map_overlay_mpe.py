#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#
# Add a map overlay to each map tile (Google maps format)
# This is necessary because the Google maps don't include a coastline.
##############################################################################  

import sys, array, Image, ImageChops

force = False

import os, string
from fn_mk_tiledir import mk_tiledir

def add_overlay( tileName, mapName ):
    tile = Image.open( tileName )
    tile = tile.convert( 'RGB' )
    map = Image.open( mapName )
    map = map.convert( 'RGB' )
    outimg = ImageChops.multiply( tile, map )
    outimg.save( tileName )
    return
    
def run( workdir = '/home/mike/wepoco/data/mpe/', sumname=None ):
    bindir='/home/mike/wepoco/bin/'
    datadir='/home/mike/wepoco/data/mpe/'
    mapdir=datadir + 'map/'
    config = 'acc.out'
    mapconfig = 'map.list'

    if not sumname:
        try:
            configf = file( workdir + config, 'r' )
            discard = string.strip( configf.readline() )
            sumname = string.strip( configf.readline() )
            lasttmp = string.strip( configf.readline() )
            configf.close()
        except:
            return (1, 'Failed to read configuration file')

        if (lasttmp == 'last'):
            islast = True
        else:
            return (2, 'Not last file of day')
        pass

    try:
        imgname = sumname + '.png'
        tiledir = mk_tiledir( workdir, sumname )
        mapconf = file( mapdir + mapconfig, 'r' )
        for mapname in mapconf:
            mapname = string.strip( mapname )
            tilename = mapname  # i.e. also a png file, but dest dir will be different */
            try:
                add_overlay( workdir + tiledir + tilename, mapdir + mapname )
            except Exception, inst:
                #print inst
                return (5, 'Failed when processing %s' % (mapname))
            pass
        pass
    except Exception, inst:
        #print inst
        return (4, 'Failed to open map config file' )
            
    return (0, 'OK')

if __name__ == "__main__":
    import sys
    force = True
    (rc, msg) = run( workdir='./', sumname=sys.argv[1] )
    print msg
    sys.exit( rc )
