#!/bin/env python

import os, time

def is_old_grb( f, now ):
    if f[0:12] == now:
        return False
    else:
        return True

def list_all_old_grb():
    # return list of all .grb (GRIB) files that haven't been
    # archived.
    fnames = os.listdir( "." )
    oldgrbs = []
    now = time.gmtime()
    now_prefix = "MPE_%d%02d%02d" % (now[0],now[1], now[2])
    for f in fnames:
        if f[-4:] == ".grb":
            if is_old_grb( f, now_prefix ):
                oldgrbs.append( f )
                pass
            pass
        pass
    return oldgrbs

oldgrbs = list_all_old_grb()
for f in oldgrbs:
    dirname = f[0:13] + f[18:23] + "_grb"
    print dirname, f
    try:
        os.mkdir( dirname )
    except:
        pass
    os.rename( f, dirname + '/' + f)
    pass

