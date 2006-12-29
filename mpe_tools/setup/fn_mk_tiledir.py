#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#

import os, string

def mk_tiledir( datadir, sumname ):
    words = string.split( sumname, '.' )
    tiledir = words[0] + '/'
    # must have subdirs for each zoom level
    try:
        os.mkdir( datadir + tiledir )
        for zoom in [3,4,5]:
            os.mkdir( datadir + tiledir + "%d" % (zoom) )
            pass
        pass
    except:
        pass # Probably already done.    
    return tiledir



