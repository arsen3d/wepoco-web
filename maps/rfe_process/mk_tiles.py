#!/usr/bin/python
# Michael Saunby.
##############################################################################  

import sys, array, Image
import os, string

# Load a data file and generate 100x100 pixel tiles
def mktiles(filename, tileprefix):
    incols = 994
    inrows = 1089
    
    rows = []
    f = file(filename)
    for r in range(inrows):
        rows.append(array.array('h'))
        rows[r].fromfile( f, incols )
        rows[r].byteswap()
        pass

    for y in range((inrows+99)/100):
        print "row", y
        for x in range((incols+99)/100):
            outmin = array.array('h')
            outmax = array.array('h')
            outdat = array.array('h')
            for j in range(100):
                for i in range(100):
                    maxv = 0
                    minv = 9000
                    # Strictly speaking should check for row or col out of
                    # 0 to inrows-1  (or incols-1)
                    for ja in range(-1,2):
                        for ia in range(-1,2):
                            try:
                                v = rows[y*100+j+ja][x*100+i+ia]
                                if v > maxv:
                                    maxv = v
                                    pass
                                if v < minv:
                                    minv = v
                                    pass
                                pass
                            except:
                                pass
                            pass
                        pass
                    try:
                        v = rows[y*100+j][x*100+i]
                    except:
                        v = 0
                        minv = 0
                        maxv = 0
                        pass
                    outdat.append(v)
                    outmin.append(minv)
                    outmax.append(maxv)
                    pass
                pass
            tiledat = "%s/%02d_%02d" % (tileprefix, y, x)
            tilemin = "%s/%02d_%02d_min" % (tileprefix, y, x)
            tilemax = "%s/%02d_%02d_max" % (tileprefix, y, x)
            print "saving tile",tiledat
            outdat.tofile(file(tiledat, "wb"))
            print "saving tile",tilemin
            outmin.tofile(file(tilemin, "wb"))
            print "saving tile",tilemax
            outmax.tofile(file(tilemax, "wb"))
            pass
        pass
    return


if __name__ == "__main__":
    import sys
    import re
    m = re.match("(\w+)\.bil$", sys.argv[1])
    try:
        os.mkdir(m.group(1))
    except:
        pass
    mktiles( sys.argv[1], m.group(1) )


