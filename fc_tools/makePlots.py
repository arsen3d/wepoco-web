#!/usr/local/badc/linux/suse10/cdat/bin/python

"""
makePlots.py
============

Usage:
======

makePlots.py -l 10,37.5 -s adis_abeba -v apcp /home/users/astephen/wepoco/data/apcp.2006072600.nc
makePlots.py -l 15,32.5 -s khartoum -v apcp /home/users/astephen/wepoco/data/apcp.2006072600.nc

"""

import vcs, cdms, cdutil, Numeric, genutil
import os, sys, getopt, MA

tlen=13
basedir="/home/users/astephen/wepoco"

def nudgeSingleValuesToAxisValues(value, axisValues, axisType):
        """
        Takes a value and checks if it is in the axisValues array. If not, it nudges the
        value to the nearest neighbour in axis. It returns the new value twice along
        with a message describing the change.
        """
        rtMessage=""

        newValue=None

        if value in axisValues:
            newValue=value
        else:
            sortedAxis=[]
            for i in axisValues:
                sortedAxis.append(i)
            sortedAxis.sort()

            if value<sortedAxis[0]:
                newValue=sortedAxis[0]
            elif value>sortedAxis[-1]:
                newValue=sortedAxis[-1]
            else:
                for i in range(len(axisValues)):
                    if i<(len(axisValues)-1):
                        (current, nextone)=(axisValues[i], axisValues[i+1])
                        if current>nextone:
                            tempc=nextone
                            nextone=current
                            current=tempc

                        if value>current and value<nextone:
                            lowergap=value-current
                            uppergap=nextone-value
                            if uppergap==lowergap:
                                newValue=nextone
                            elif uppergap>lowergap:
                                newValue=current
                            elif uppergap<lowergap:
                                newValue=nextone
                            break
            if newValue==None:
                raise ("Could not nudge selected value '%s' into axis '%s'." % (value, axisType)
)
            rtMessage="%s axis selected value '%s' nudged to nearest value in real axis '%s' ;" % (axisType, value,
 newValue)
            print rtMessage

        return (newValue, newValue, rtMessage)


def parseArgs(args):
    if args[0].find("makePlots.py")>-1: args=args[1:]
    # Set up defaults
    lat=None
    lon=None
    var=None
    location=None

    argList, inputFileList=getopt.getopt(args, "l:v:s:")    
    infile=inputFileList[0]
    for arg,value in argList:
        if arg=="-l":
            lat,lon=[float(i) for i in value.split(",")]
        elif arg=="-v":
            var=value
        elif arg=="-s":
            location=value

    return (infile, var, lat, lon, location)

def accumulate24Hourly(data):
    """Returns 12-hourly data accumulated to 24-hours."""
    newTimeValues=[]
    taxis=data.getTime()
    tunits=data.units
    print len(data.getTime())
    newarray=[]

    for i in range((tlen/2)):
        p1=data(time=slice(i,i+1))
        p2=data(time=slice(i+1,i+2))
        accum=p1+p2
        newarray.append(accum)
        newTimeValues.append(p2.getTime()[0])

    array=MA.concatenate(newarray)
    array=MA.array(array, 'f', fill_value=data.getMissing())
    axes=data.getAxisList()
    newTimeAxis=cdms.createAxis(newTimeValues)
    newTimeAxis.units=tunits
    newTimeAxis.designateTime()
    newTimeAxis.id=newTimeAxis.long_name=newTimeAxis.title="time"
    
    newaxes=[newTimeAxis]+axes[1:]
    var=cdms.createVariable(array, axes=newaxes, id=data.id)
    for att in ("units", "long_name"):
        setattr(var, att, getattr(data, att))
    return var 


def getVariable(infile, var, lat, lon):
    """Get the variable needed for the location (lat, lon)."""

    datafile=cdms.open(infile)
    if var==None:
        var=datafile.listvariables()[0]

    metadata=datafile[var]
    latax=metadata.getLatitude()[:]
    lonax=metadata.getLongitude()[:]
    lat=nudgeSingleValuesToAxisValues(lat, latax, "latitude")[0]
    lon=nudgeSingleValuesToAxisValues(lon, lonax, "longitude")[0]

    data=datafile(var, lat=lat, lon=lon, squeeze=1)
    print data.id
    data=data(time=slice(0,tlen))
    data=accumulate24Hourly(data)
    datafile.close()

    # Do some working with the data depending on the variable
    if var=="tmpk":  # ncep temperature
        data[:]=data[:]-270.
        data.units="degC"
    elif var=="apcp": # ncep rainfall
        # fix < zeros
        newarray=[]
        count=0
        for i in data:
            newarray.append([])
            for x in i: 
                x=x[0]
                if x<0.0: 
                    x=0.0  
                newarray[count].append(x)
            count=count+1
        data[:]=Numeric.array(newarray, 'f')
    return (data,lat,lon)


def calculateStats(var):
    """Creates the statistical outputs needed."""
    print "Taking ensemble average as main line, max, min as one lot and +/- standard dev as other."
    cdms.setAutoBounds("on")
    av=cdutil.averager(var, axis="1")
    stddev=genutil.statistics.std(var, axis="1")
    cdms.setAutoBounds("off")

    maxList=[]
    minList=[]
    stddevUpper=[av[i]+stddev[i] for i in range(len(av))]
    stddevLower=[av[i]-stddev[i] for i in range(len(av))]

    for t in var:
        (mini, maxi)=vcs.minmax(t)
        minList.append(mini)
        maxList.append(maxi)
     
    return (av, maxList, minList, stddevUpper, stddevLower)


def writeOutput(infile, var, lat, lon, dav, dmax, dmin, sdupper, sdlower, location):
    """
    Writes an output file of the variables generated.
    """

    location=location.replace(" ","_").lower()
    f=cdms.open(infile)
    
    mapit={"apcp":("rainfall","l/m^2"), "tmpk":("temperature","K")} 
    varname=mapit[var][0]
    units=mapit[var][1]
    datetime=os.path.split(infile)[-1].split(".")[1]
    outfile="%s_%s_%s.nc" % (datetime, location, varname)
    outpath=os.path.split(infile)[0]
    outfile=os.path.join(outpath, outfile)
    fout=cdms.open(outfile, "w")
    latax=cdms.createAxis([lat])
    latax.units="degrees_north"
    latax.id=latax.standard_name=latax.long_name="latitude"
    lonax=cdms.createAxis([lon])
    lonax.units="degrees_east"
    lonax.id=lonax.standard_name=lonax.long_name="longitude"   
    tax=f[var].getTime() #f(var, level=slice(0,1), lat=slice(0,1), lon=slice(0,1)).getTime()
    timeax=cdms.createAxis(Numeric.array(tax[0:tlen],'d'))
    timeax.designateTime()
    timeax.units=tax.units
    #timeax.id=timeax.standard_name=timeax.long_name="time"
    timeax.id="time"
    timeax.title=tax.title
    timeax.delta_t=tax.delta_t
    timeax.init_time=tax.init_time
    timeax.actual_range=tax.actual_range
    del timeax.axis
    del timeax.calendar
    metadata=f[var]
    fv=metadata.missing_value
    newshape=(len(timeax), len(latax), len(lonax))
    
    maxFound=20. # Set as our max value if not greater
    
    for v in ((dav, "average"), (dmax, "maximum"), (dmin, "minimum"), \
      (sdupper, "plus_std_dev"), (sdlower, "minus_std_dev"), ("always10", "always10")):
        if type(v[0])==type("jlj") and v[0]=="always10": 
            print "Creating always equal to 10 variable."
            always10=MA.zeros(newshape, 'f')+10.
            #print always10.shape, dav.shape, type(dav)
            newvar=cdms.createVariable(always10,  axes=[timeax, latax, lonax], id=v[1], fill_value=fv)
            newvar.longname="always10"
        else:
            data=v[0]
            name=varname+"_"+v[1]
            if not type(data)==type([1,2]):
                data=data(squeeze=1)
            data=MA.resize(data, newshape)
            newvar=cdms.createVariable(data, axes=[timeax, latax, lonax], id=name, fill_value=fv)
            newvar.long_name="%s - %s" % (varname.title(), v[1].replace("_", " "))
            newvar.units=metadata.units

        (dummy,vmax)=vcs.minmax(newvar)
        if vmax>maxFound:
            maxFound=vmax
        fout.write(newvar)
        fout.sync()
        del newvar

    fout.close()
    return (outfile, varname, datetime, maxFound)

def ferretPaths():
    return """export FER_DIR=/home/users/astephen/wepoco/external/ferret ; export FER_DSETS=/home/users/astephen/wepoco/external/ferret/data ; export PATH=".:/usr/local/NDG/cdat4.0_cdunifpp0.6/bin:/usr/local/badcdat/bin:/usr/local/bin:/home/users/astephen/:/usr/bin:/bin:/usr/sbin:/sbin:/usr/bin/X11:/usr/kerberos/bin:/home/users/astephen/scripts:/usr/local/hdf/bin:/usr/local/grads/bin:/home/users/astephen/wgrib_linux:/usr/local/nco/bin:/usr/kerberos/bin:/usr/local/bin:/bin:/usr/bin:/usr/X11R6/bin:/home/users/astephen/wepoco/external/ferret/bin:$FER_DIR/bin"; export FER_WEB_BROWSER="netscape -ncols 60"; export FER_EXTERNAL_FUNCTIONS="$FER_DIR/ext_func/libs"; export FER_GO=". $FER_DIR/go $FER_DIR/examples $FER_DIR/contrib"; export FER_DATA=". $FER_DSETS/data $FER_DIR/go $FER_DIR/examples $FER_DIR/contrib /data/ncep"; export FER_DESCR=". $FER_DSETS/descr"; export FER_GRIDS=". $FER_DSETS/grids"; export TMAP="$FER_DIR/fmt"; export PLOTFONTS="$FER_DIR/ppl/fonts"; export SPECTRA="$FER_DIR/ppl" ; export FER_PALETTE=". $FER_DIR/ppl"  """ 


def makePlot(ncfile, varname, lat, lon, datetime, location, maxValue):
    """
    Writes and executes a ferret script to generate plot.
    """
    maxv=int(maxValue)
    if maxv<maxValue: maxv=maxv+1
    maxValue=maxv    
    location=location.replace(" ","_").lower()
    titlename=varname.title()
    nlocation=location.replace("_", " ")
    nlocation=nlocation.title()
    plotfile=os.path.split(ncfile)[-1][:-3]+".gif"
    plotfile=os.path.join(basedir, "plots", plotfile)
    
    ferretScript="""SET DATA "%s"
SET WINDOW/SIZE=0.1
DEFINE VIEWPORT/XLIM=0.12,1./YLIM=0,1. myvp
SET VIEWPORT myvp
PPL AXLSZE,0.15,0.15
PPL TXLSZE,0.13 
! Note - to change vertical tics use VLIM=min:max:step such as 0:40:10 in PLOT args
PLOT/Y=%s/X=%s/VLIM=0:%s/NOLAB/TITLE="%s - NCEP %s Forecasts" %s_maximum

go plot_swath poly/over/pal=cyan/nolab %s_minimum, %s_maximum
go plot_swath poly/over/pal=blue/nolab %s_minus_std_dev %s_plus_std_dev

let ymax ($yaxis_max)

!go legline 8650 30 `0.9*ymax` 5 0.15 "Maximum"
!go legline 8650 30 `0.85*ymax` 4 0.15 "Plus 1 std dev"
!go legline 8650 30 `0.8*ymax` 7 0.15 "Average"
!go legline 8650 30 `0.75*ymax` 4 0.15 "Minus 1 std dev"
!go legline 8650 30 `0.7*ymax` 5 0.15 "Minimum"

LABEL 8730,`0.5*ymax`,0,0,0.22 "mm"

PLOT/OVER/Y=%s/X=%s/NOLAB/LINE=5 %s_maximum
PLOT/OVER/Y=%s/X=%s/NOLAB/LINE=5 %s_minimum
PLOT/OVER/Y=%s/X=%s/NOLAB/LINE=4 %s_plus_std_dev
PLOT/OVER/Y=%s/X=%s/NOLAB/LINE=4 %s_minus_std_dev
PLOT/OVER/Y=%s/X=%s/NOLAB/LINE=13 %s_average
!PLOT/OVER/Y=%s/X=%s/NOLAB/LINE=1 %s_minimum
PLOT/OVER/Y=%s/X=%s/NOLAB/LINE=1 always10

FRAME/FORMAT=GIF/FILE="%s"
CANCEL VIEWPORT

""" % (ncfile, lat, lon, maxValue, nlocation, titlename, varname,
              varname, varname, varname, varname,
              lat, lon, varname,
              lat, lon, varname,
              lat, lon, varname,
              lat, lon, varname,
              lat, lon, varname, 
              lat, lon, varname, lat, lon, plotfile)

    os.chdir(os.path.join(basedir, "fscripts"))
    ferretFile="%s_%s.jnl" % (location, datetime)
    ferretPath=os.path.join(basedir, "fscripts", ferretFile)
    output=open(ferretPath, "w")
    output.write(ferretScript)
    output.close()
   
    print "Running ferret script:", ferretPath
    cmd="%s ; cd %s;  /home/users/astephen/wepoco/external/ferret/bin/ferret -gif -script %s" % (ferretPaths(), os.getcwd(), ferretFile)
    print cmd
    print "\n\n"
    os.system(cmd)
    print "\nDONE\n"
    return plotfile 

if __name__=="__main__":
    #print "makePlot.py -l 10,37.5 -s adis_abeba -v apcp /home/users/astephen/wepoco/data/apcp.2006072600.nc".split()
    args=sys.argv[1:]
    if len(args)<6: 
        print __doc__
        sys.exit()
 
    (infile, var, lat, lon, location)=parseArgs(args)
    (data,newlat,newlon)=getVariable(infile, var, lat, lon)
    (dav, dmax, dmin, sdupper, sdlower)=calculateStats(data)
    (outfile, realvar, datetime, maxValue)=writeOutput(infile, var, newlat, newlon, dav, dmax, dmin, sdupper, sdlower, location)
    print "Wrote...", outfile
    plotfile=makePlot(outfile, realvar, newlat, newlon, datetime, location, maxValue)
    print "Plotted to file:", plotfile
