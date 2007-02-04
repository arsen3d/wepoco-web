#!/usr/local/badc/linux/suse10/cdat/bin/python

"""
getNPlot.py
==============

Gets data from NCEP based on a datetime or the latest day (today)
at 00hours.

Usage
=====

    getNPlot.py [-l] [-d <YYYYMMDDHH>]
    
Where
=====

	-l	- gets the current day at 00hours.
	YYYYMMDDHH	- date and time.

"""

import os, commands, sys, re,time
import cdms, vcs, ftplib, shutil

import parseMarkersXML

os.environ["http_proxy"]="http://wwwcache2.rl.ac.uk:8080"
os.environ["PATH"]="/usr/local/badc/linux/suse10/cdat/bin:/usr/bin"
basedir="/home/users/astephen/wepoco"

def exitNicely(msg):
    print __doc__
    print msg
    sys.exit()


def getDaysMinus(dateTime, n):
    "Returns n days before the dateTime string."
    d=dateTime
    (y,m,d,h)=(int(d[:4]),int(d[4:6]),int(d[6:8]),int(d[8:10]))
    newday=time.strftime("%Y%m%d00", time.localtime(time.time()-(n*86400)))
    return newday


def downloadFiles(dateTime):
    """Downloads data files from NCEP for the dateTime specified."""
    print "For:", dateTime

    datadir=os.path.join(basedir, "data")
    os.chdir(datadir)
    hostname, basepath="ftp.cdc.noaa.gov","Datasets.other/map/ENS"

    pathlist=[]
    for pref in ("apcp", "t850"):
        filename="%s.%s.nc" % (pref, dateTime)
        myversion=os.path.join(datadir, filename)
        if os.path.isfile(myversion) and os.path.getsize(myversion)>7500000:
            print "Local version already exists:", myversion
        else:
            try:
                host=ftplib.FTP(hostname, "anonymous", "a.stephens@rl.ac.uk")
                host.cwd(basepath)
                host.retrbinary('RETR %s' % filename, open(filename, 'wb').write)    
            except:
                yesterday=getDaysMinus(dateTime, 1)
                print "Re-using yesterday's files...as not on FTP server..."
                yfname="%s.%s.nc" % (pref, yesterday)
                yfile=os.path.join(datadir, yfname)
                shutil.copy(yfile, myversion)
                
            print "Got file:", myversion 
        pathlist.append(myversion)

    return pathlist
    

def createPlots(rainfile, tempfile, dateTime):
    "Creates plots for sample locations."
    plotlist=[]

#    africaSites={"Khartoum":[15.594, 32.531], "Adis_Abeba":[9.022, 38.794]}
#    for site in [("khartoum", (15,32.5)), ("adis_abeba", (10,37.5))]:
    siteDict=parseMarkersXML.parseMarkers()
    for location, (lat, lon) in siteDict.items():
        fstring=location.lower().replace(" ","_")
        #(location, (lat,lon))=site
        cmd=("/home/users/astephen/wepoco/scripts/makePlots.py -l %s,%s -s \"%s\" -v %s %s" % (lat, lon, location, "apcp", rainfile))
        print "\n", cmd
        os.system(cmd)
        plotfile="/home/users/astephen/wepoco/plots/%s_%s_%s.gif" % (dateTime, fstring, "rainfall")
        plotlist.append(plotfile)
    return plotlist


def scopyToFoehn(plotlist):
    "Copies the plots to foehn's webserver"
    print plotlist
    for f in plotlist:
        os.chmod(f, 0644)
        print "Copying...", os.path.split(f)[-1]
	os.system("/usr/bin/scp %s astephen@foehn.badc.rl.ac.uk:/var/www/home_site/astephens/ncep_data" % f)
	 

def main(dateTime):
    "Controls it all."
    datafiles=downloadFiles(dateTime)
    plotlist=createPlots(datafiles[0], datafiles[1], dateTime)
    scopyToFoehn(plotlist)
    
    

if __name__=="__main__":
    dateTime=None
    args=sys.argv[1:]
    if args[0]=="-l":
	dateTime=time.strftime("%Y%m%d00", time.localtime(time.time()))
    elif args[0]=="-d":
        dt=args[1]
	if len(dt)!=10: raise "Must give datetime as 10 numbers"
	try:
	    test=long(dt)
	except:
	    raise "Must give datetime as 10 numbers"
	dateTime=dt

    if not dateTime: exitNicely("Error: must provide -l argument of datetime after -d arg.")
 
    main(dateTime)

