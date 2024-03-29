#!/usr/bin/python
# Michael Saunby.
##############################################################################  

import sys, array, Image
import os, string

# Composite 36 100x100 tiles

empty = array.array('h')
for i in range (100*100):
    empty.append(-1024)
    pass

def readtile(filename):
    matrix = array.array('h')
    try:
        matrix.fromfile( file(filename), 100*100 )
        return matrix
    except:
        return empty

def composite(yr,suffix=""):
    for y in range(11):
        for x in range(10):
            tile = "%02d_%02d%s" % (y,x,suffix)
            matrices = []
            for mo in range(12):
                for dk in range(3):
                    name = "a%s%02d%drf/%s" % (yr,(mo+1),(dk+1),tile)
                    print name
                    matrices.append(readtile(name))
                    pass
                pass
            print len(matrices)
            v = array.array('h')
            for p in range(100*100):
                for d in range(36):
                    v.append(matrices[d][p])
                    pass
                pass
            print len(v)
            outname = "RFE_20%s_%02d_%02d%s" % (yr, y, x, suffix)
            v.tofile(file(outname,"wb"))
            pass
        pass
    return

if __name__ == "__main__":
    import sys
    year = sys.argv[1]  # e.g. "09"
    composite(year)
    composite(year,"_min")
    composite(year,"_max")



