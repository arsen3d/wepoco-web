#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#
# This script should be called by cron after each new mpe grib file
# has been downloaded.
#
##############################################################################  

import sys, shutil, array

# Copy from src file to dst file translating 9999.0 to 0.0
def copy_data( srcf, dstf ):
    eof = False
    while eof == False:
        data = array.array( 'd' )
        # 'fromfile' raises EOFError at end of file
        try:
            data.fromfile( srcf, 1024 )
        except EOFError:
            eof = True
            pass        
        idx = 0
        for x in data:
            if x == 9999.0:
                data[idx] =  0.0
            idx = idx + 1
            pass
        data.tofile( dstf )
        pass
    return
    
def add_incr( sumf, incrf, tmpf ):
    eof = False
    while eof == False:
        sumbuf = array.array( 'd' )
        data = array.array( 'd' )
        # 'fromfile' raises EOFError at end of file
        try:
            sumbuf.fromfile( sumf, 1024 )
        except EOFError:
            eof = True
            pass
        try:
            data.fromfile( incrf, 1024 )
        except EOFError:
            pass
        
        idx = 0
        for x in data:
            if x !=  9999.0:
                sumbuf[idx] =  sumbuf[idx] + x
                pass
            idx = idx + 1
            pass
        
        sumbuf.tofile( tmpf )
        pass
    return

import os, string

def run( datadir='/home/mike/wepoco/data/mpe/', gribname=None, sumname=None ):
    bindir='/home/mike/wepoco/bin/'
    config = 'fetch.out'
    incname = 'tmp.flt'


    if not gribname:
        try:
            configf = file( datadir + config, 'r' )
            gribname = string.strip( configf.readline() )
            sumname = string.strip( configf.readline() )
            configf.close()
        except:
            return (1, 'Failed to read configuration file')
        pass
    
    try:
        gribf = file( datadir + gribname, 'r' )
    except:
        return (2, 'Failed to open grib file ' + gribname )

    # Ideally use Python interface to grib library
    # For now do this.
    gribf.close()
    rc = os.system( bindir + 'dump_mpe_grib ' + datadir + gribname + ' ' + datadir + incname + ' >/dev/null' )
    if rc != 0:
        return (1, 'dump_mpe_grib failed')

    # Add the floating point dump to the total
    #
    incfile = file( datadir + incname, 'rb' )
    try:
        # Open sum file read only because we create a new file with the new sum
        # and then replace old with new.
        sumfile = file( datadir + sumname, 'rb' )
    except:
        # Assume that we are to start a new total
        sumfile = file( datadir + sumname, 'wb' )
        copy_data( incfile, sumfile )
        return (0, 'OK')

    try:
        newfile = file( datadir + sumname + '~', 'wb' )
        add_incr( sumfile, incfile, newfile )
        newfile.close()
        sumfile.close()
        incfile.close() 
        shutil.move( datadir + sumname + '~', datadir + sumname )
    except:
        return (2, 'dump_mpe_grib failed in incr')

    try:
        os.remove( datadir + config )
    except:
        pass
    
    return (0, 'OK')

if __name__ == "__main__":
    import sys
    for gribname in sys.argv[1:]:
        sumname = gribname[0:12] + gribname[17:23] + '.acc'
        (rc, msg) = run( datadir='./', gribname=gribname, sumname=sumname )
        print msg
        pass
    sys.exit( rc )
