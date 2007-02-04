#!/usr/local/badc/linux/suse10/cdat/bin/python

"""
createTiles.py
==============

Can re-open files with:

import array
x=array.array('f')
fin=open("/home/users/astephen/wepoco/data/rainfall/20060924/rainfall.2006092400.288.0h.dat", "rb")
x.fromfile(fin, (35*33))

"""


import time,os,sys,cdms,Numeric,array,MA
import scopy
basedir="/home/users/astephen/wepoco"
datadir=os.path.join(basedir, "data")
rainfalldir=os.path.join(datadir, "rainfall")

def processRainfall(file, outdir, var, north, west, south, east):
    "Subsets, averages, writes to binary files."
    f=cdms.open(file)
    v=f(var, lat=(south, north), lon=(west, east))
    timevalues=v.getTime()[:]
    t0=timevalues[0]
    # I need to test if step 0 always has only missing values
    # remove -50 values???
    v=MA.masked_less(v,0)
    # create average of all ensemble members
    av=MA.average(v, axis=1)

    # get stuff for name
    datetime=os.path.split(file)[-1].split(".")[1]

    outpaths=[]

    # now step through time dimension (0)
    count=0
    for dslice in av:
        ts=timevalues[count]-t0
        outfile="rainfall.%s.%dh.dat" % (datetime, ts)
        outpath=os.path.join(outdir, outfile)
        count=count+1
        numarray=Numeric.array(dslice._data)
        sh=numarray.shape
        length=sh[0]*sh[1]
        flatarray=Numeric.resize(numarray, [length])
        output=open(outpath, "wb")
        arr=array.array('f', flatarray)
        arr.tofile(output)
        output.close()
        print "Written:", outpath
        outpaths.append(outpath)

    return outpaths


def getNow():
    "Returns now as YYYYMMDD string."
    return time.strftime("%Y%m%d", time.localtime(time.time()))

def getYesterday():
    "Returns yesterday as YYYYMMDD string."
    oneday=60*60*24
    now=time.time()
    yesterday=time.localtime((now-oneday))
    return time.strftime("%Y%m%d", yesterday)

if __name__=="__main__":
    args=sys.argv[1:]
    if len(args)>0:
        t=args[0]
    else:
        t=getYesterday()
    infile="apcp.%s00.nc" % t
    inpath=os.path.join(datadir, infile)
    outdir=os.path.join(rainfalldir, t)
    if not os.path.isdir(outdir):    os.mkdir(outdir)
    outpaths=processRainfall(inpath, outdir, "apcp", 42.5, -22.5, -42.5, 
57.5)  
    scopy.scopy(outpaths, "/var/www/home_site/astephens/ncep_data/data/")
