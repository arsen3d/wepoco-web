#!/usr/local/badc/linux/suse10/cdat/bin/python

"""
scopy.py
==============

Copies a file to a remote machine.
"""

import os, commands, sys, re,time
import cdms, vcs, ftplib

basedir="/home/users/astephen/wepoco"

def scopy(sources, target):
    "Copies the plots to foehn's webserver"
    
    for source in sources:
        os.chmod(source, 0644)
        print "Copying...", os.path.split(source)[-1]
	os.system("/usr/bin/scp %s astephen@foehn.badc.rl.ac.uk:%s" % (source, target))
	 
   
if __name__=="__main__":
    sources=sys.argv[1:-1]
    target=sys.argv[-1]
    scopy(sources, target)
    
