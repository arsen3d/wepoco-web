#!/usr/bin/python
# Michael Saunby.
##############################################################################  

import sys, array, Image
import string
from os import popen2

def mkcsv(yr, f):
    (prin, prout) = popen2("proj +proj=aea +lat_1=-19 +lat_2=21 +lat_0=1 +lon_0=20 +x_0=0 +y_0=0 +units=m +ellps=clrk66 +to_meter=8000 +no_defs")
    for i in range(20):
        prin.write("%d 0\n" % (i));
    prin.close();
    for li in prout:
        print li
        pass

if __name__ == "__main__":
    import sys
    # year outfile
    mkcsv( sys.argv[1], sys.argv[2] )


