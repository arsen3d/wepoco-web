#!/usr/local/badc/linux/suse10/cdat/bin/python

from xml.dom import minidom
import os,sys,re

def parseMarkers(mfile="/home/users/astephen/wepoco/data/markers.xml"):
    "Parses markers - returns a dict of key/value of name/(lat,lon)."
    d={}
    """root=minidom.parse(mfile)
    mNodes=root.getElementsByTagName("markers")[0]
    for n in mNodes:
        print n.getElementsByTagName("marker")[0].childNodes[0].nodeValue 
    """
    patn=re.compile('<marker label="(.*)" location=".*" lat="(.*)" lng="(.*)" level')
    for line in open(mfile).readlines():
        if line.find("markers")>-1: continue
        m=patn.search(line)
        if m:
            (loc,lat,lon)=m.groups() 
            d[loc]=(lat,lon)
    return d 

if __name__=="__main__":
    print parseMarkers()
