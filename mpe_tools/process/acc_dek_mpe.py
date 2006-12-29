#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#

##############################################################################  

import sys, array, shutil

force = False

def dekname( sumname ):
    daynum = int(sumname[10:12])
    if daynum < 11:
        deknum = 1
    elif daynum < 21:
        deknum = 2
    else:
        deknum = 3
        pass
    return "%s_DEK%d.acc" % (sumname[0:10], deknum)

def start_of_dekad( sumname ):
    daynum = int(sumname[10:12])
    if (daynum == 1) or (daynum == 11) or (daynum == 21):
        return True
    return False

def add_data( infileA, infileB, logfile ):

    # Note these files are based on standard Meteosat projection
    # with true width and height of 2500 but with 100 pixels cropped
    # from each edge of the image.
    #
    #width = 2300
    #height = 2300

    width = 3712
    height = 3712
    

    dataA = array.array( 'd' )
    dataA.fromfile( infileA, width*height )

    dataB = array.array( 'd' )
    dataB.fromfile( infileB, width*height )

    dataResult = array.array( 'd' )
    
    idx = 0
    for a in dataA:
        b = dataB[ idx ]
        idx = idx + 1
        dataResult.append( a + b )

    del(dataA)
    del(dataB)

    return dataResult


import os, string


def run(datadir='/home/mike/wepoco/data/mpe/', sumname=None,  verbose=False):
    bindir='/home/mike/wepoco/bin/'
    config = 'acc.out'

    if not sumname:
        try:
            configf = file( datadir + config, 'r' )
            discard = string.strip( configf.readline() )
            sumname = string.strip( configf.readline() )
            lasttmp = string.strip( configf.readline() )
            configf.close()
            imgname = sumname + '.png'
            if verbose:
                print "# sumname=", sumname
                pass
            pass
        except:
            return (1, 'Failed to read configuration file')
        
        if (lasttmp != 'last'):
            return (2, 'Not last file of day')
        pass
    
    try:
        # Open sum file.
        sumfile = file( datadir + sumname, 'rb' )
    except:
        return (3, 'Failed to open sum file')

    if start_of_dekad( sumname ):
        if verbose:
            print "# start of dekad", dekname( sumname )
            pass
        shutil.copyfile( datadir + sumname, datadir + dekname( sumname ) )
        pass
    else:
        try:
            if verbose:
                print "# adding to dekad", dekname( sumname )
                pass
            # Open dekad acc file.
            dekfile = file( datadir + dekname( sumname ), 'rb' )
            result = add_data( sumfile, dekfile, None )
            dekfile.close()
            dekfile = file( datadir + dekname( sumname ), 'wb' )
            result.tofile( dekfile )
            dekfile.close()
        except Exception, inst:
            if verbose:
                print inst
            return (4, 'Failed to update dekad sum file %s' % dekname( sumname ))
        pass
    
    return (0, 'OK')

if __name__ == "__main__":
    import sys
    force = True
    datadir = "./"
    for sum in sys.argv[1:]:
        print "processing for", sum
        (rc, msg) = run(datadir, sumname=sum, verbose=True)
        print msg
        pass
    sys.exit( rc )


