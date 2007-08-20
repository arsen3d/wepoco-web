#!/usr/bin/python
# Michael Saunby. For Wepoco.
#
##############################################################################  

# Settings for the local processing server.
my_datadir='/home/mike/wepoco/data/mpe/'


# Settings for the remote web server. 
# Read from configuration file.
my_site='www.wepoco.com'
my_untar='/maps/untar.php?tgz='
my_ftp_host='' # e.g. saunby.net
my_ftp_user='' ' e.g. wepoco
my_ftp_passwd='' e.g. password1

#############################################################################

force = False

import sys, os, string, httplib
from fn_mk_tiledir import mk_tiledir

def run():
    datadir=my_datadir
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

        arfile = file( datadir + archive, "rb" )
        ftp = FTP( my_ftp_host )
        ftp.login( my_ftp_user, my_ftp_passwd )
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

    return (0, 'OK')

if __name__ == "__main__":
    import sys
    force = True
    (rc, msg) = run()
    print msg
    sys.exit( rc )


