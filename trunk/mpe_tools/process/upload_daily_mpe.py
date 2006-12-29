#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#

##############################################################################  

force = False

import sys, os, string, httplib
from fn_mk_tiledir import mk_tiledir

def untar( tarfile ):
    site='www.wepoco.com'
    url='/maps/untar.php?tgz='
    conn = httplib.HTTPConnection( site )
    conn.request( 'GET', url + tarfile )
    r1 = conn.getresponse()
    return 0

def run():
    datadir='/home/mike/wepoco/data/mpe/'
    config = 'acc.out'

    try:
        configf = file( datadir + config, 'r' )
        discard = string.strip( configf.readline() )
        sumname = string.strip( configf.readline() )
        lasttmp = string.strip( configf.readline() )
        configf.close()
        tiledir = mk_tiledir( datadir, sumname )
    except:
        return (1, 'Failed to read configuration file')

    if (lasttmp == 'last') or force:
        islast = True
    else:
        return (2, 'Not last file of day')


    try:
        archive = tiledir[:-1] + ".tgz"

        # Create an archive of tiledir using the tar command
        os.system( "cd " + datadir + ";tar czf " + archive + " " + tiledir )
    except:
        return (3, 'tar failed')

    try:
        from ftplib import FTP

        user = "wepoco%saunby.net"
        host = "saunby.net"
        passwd = "w34h72"

        arfile = file( datadir + archive, "rb" )
        ftp = FTP( host )
        ftp.login( user, passwd )
        ftp.cwd( "mpe" )
        ftp.storbinary("STOR " + archive, arfile )
        arfile.close()
        ftp.close()

    except Exception, inst:
        # Print the error message.  It wouldn't be the first time
        # that quota is exceeded.
        print "ftp failed for", archive
        print inst
        # Use 0 return as other progs need to run even if this fails
        return (0, 'ftp failed: ' + inst )

    try:
        untar( archive );
    except:
        # Use 0 return as other progs need to run even if this fails
        return (0, 'untar failed')
    
    return (0, 'OK')

if __name__ == "__main__":
    import sys
    force = True
    (rc, msg) = run()
    print msg
    sys.exit( rc )


