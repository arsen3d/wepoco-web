#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#

##############################################################################  

force = False

import sys, os, string
from fn_mk_tiledir import mk_tiledir

def run( prefix=None ):
    datadir='/home/mike/wepoco/data/mpe/'

    islast = False
    
    if prefix==None:
        config = 'acc.out'
        try:
            configf = file( datadir + config, 'r' )
            discard = string.strip( configf.readline() )
            sumname = string.strip( configf.readline() )
            lasttmp = string.strip( configf.readline() )
            configf.close()
            if (lasttmp == 'last'):
                islast = True
                pass
        except:
            return (1, 'Failed to read configuration file')
        pass
        
    if islast or force:
        try:
            print "doing stuff.."
            #archive = tiledir[:-1] + ".tgz"
            ## Create an archive of tiledir using the tar command
            #os.system( "cd " + datadir + ";tar czf " + archive + " " + tiledir )
        except:
            return (3, 'tar failed')

    else:
        return (2, 'Not last file of day')

    return (0, 'OK')

if __name__ == "__main__":
    import sys

    force = True
    (rc, msg) = run( sys.argv[1])
    print msg
    sys.exit( rc )


