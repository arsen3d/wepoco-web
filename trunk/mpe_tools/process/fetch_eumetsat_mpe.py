#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#
# This script should be called by cron every half hour.  It
# downloads the latest satellite rain rate estimate (MPE).
#
# For more information on MPE products see -
# http://www.eumetsat.int/idcplg?IdcService=SS_GET_PAGE&nodeId=504&l=en
# http://www.eumetsat.int/idcplg?IdcService=SS_GET_PAGE&ssDocName=SP_1119538666663&l=en&ssTargetNodeId=
# 

#
# Configuration
#

sat_id = "M8"
#sat_id = "M9"
minute_is_last = 30  # Which slot to treat as last.


import sys, time, httplib, shelve

datadir='/home/mike/wepoco/data/mpe/'
config = 'fetch.out'
config2 = 'acc.out'
site = 'oiswww.eumetsat.int'
url_prefix = "/~idds/data/grib/"

data_retry = []
data_received = []

def read_db():
    global data_retry
    global data_received
    database = shelve.open( datadir + 'mpe_status_db' )
    try:
        data_retry = database['retry']
    except:
        data_retry = []
        pass
    try:
        data_received = database['received']
    except:
        data_received = []
        pass
    # database['retry'] = data_retry
    # database['received'] = data_received
    # print "read", data_retry
    # print "read", data_received
    database.close()
    return

def write_db():
    database = shelve.open( datadir + 'mpe_status_db', writeback=True )
    database['retry'] = data_retry
    database['received'] = data_received
    database.close()    
    # The remaining code writes an XML version
    # of the above.  It's recommended that Python programs
    # use the "shelve" version, this is just for web display.
    databasexml = file( datadir + 'mpe_status.xml', 'w' )
    databasexml.write( '<status>\n' )
    databasexml.write( '  <retry>\n' )
    for r in data_retry:
        (u,a) = r
        #print r, u, a
        databasexml.write( '  <item url="%s" acc="%s" />\n' % (u,a) )
    databasexml.write( '  </retry>\n' )
    databasexml.write( '  <received>\n' )
    for r in data_received:
        (u,a) = r
        #print r, u, a
        databasexml.write( '  <item url="%s" acc="%s" />\n' % (u,a) )
    databasexml.write( '  </received>\n' )    
    databasexml.write( '</status>\n' )
    databasexml.close()
    return

def download( url_fname, acc_fname, islast ):
    #print datadir
    conn = httplib.HTTPConnection( site )
    conn.request( 'GET', url_prefix + url_fname )
    r1 = conn.getresponse()
    if r1.status == 200:
        savef = file( datadir + url_fname, 'wb' )
        savef.write( r1.read() )
        savef.close()
        conn.close()
        configf = file( datadir + config, 'w' )
        configf.write( url_fname + '\n' )
        configf.write( acc_fname + '\n' )
        configf.close()
        config2f = file( datadir + config2, 'w' )
        config2f.write( url_fname + '\n' )
        config2f.write( acc_fname + '\n' )
        if islast:
            config2f.write( 'last\n' )
        else:
            config2f.write( '#\n' )
            pass
        config2f.close()
        pass
    return r1.status
    

def run():
    islast = False
    read_db()

    # Need time in GMT (not local)
    (year, month, day, hour, minute, z,z,z,z) = time.gmtime()
    if minute > 30:
        minute = 30
    else:
        minute = 0
        pass

    if sat_id == "M7":
        # M7 MPE files were coded to end at 2400 rather than start at 0000
        # i.e. first file of the day is 0030, last is 2400
        if (hour == 0) and (minute == 0):
            # Need yesterday (1 hour earlier will do) 
            (year, month, day, z, z, z,z,z,z) = time.gmtime(time.time() - 60*60)
            hour = 24
            minute = 0
            islast = True
            pass
        pass
    else:
        if (hour == 23) and (minute == minute_is_last):
            islast = True
            pass
        pass

    # Before downloading latest, do the retries

    # Remove any that are too old (>24 hrs)
    #purge_old_retries()

    for (url_retry, acc_retry) in data_retry:
        #print "retry", url_retry, acc_retry
        pass
    
    url_fname = 'MPE_%4d%02d%02d_%02d%02d_%s_00.grb' % (year,month,day,hour,minute,sat_id)
    acc_fname = 'MPE_%4d%02d%02d_%s_00.acc' % (year,month,day,sat_id)

    try:
        status = download( url_fname, acc_fname, islast )
    except:
        print "Unexpected error with", url_fname
        status = 999:
        pass

    if status == 200:
        # Record success (for further processing)
        data_received.append((url_fname, acc_fname))
        to_process = True
    else:
        # Record failure for retry later
        data_retry.append((url_fname, acc_fname))
        # Return error indicator and log message 
        pass

    write_db()

    if status == 200:
        return (0, '')
    else:
        return (1, '%d when fetching %s' % (status, url_fname))


if __name__ == "__main__":
    import sys
    datadir='/home/mike/wepoco/test/'
    (rc, msg) = run()
    print msg
    sys.exit( rc )
