#!/usr/bin/python
# Michael Saunby.
##############################################################################  

import sys, array, Image
import os, string

# Composite 36 100x100 tiles

def readtile(filename):
    matrix = array.array('h')
    matrix.fromfile( file(filename), 100*100 )
    return matrix

def composite(yr,suffix=""):
    for y in range(10):
        for x in range(9):
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
    composite("09")
    composite("09","_min")
    composite("09","_max")



