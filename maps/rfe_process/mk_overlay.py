#!/usr/bin/python
# Michael Saunby.
##############################################################################  

import sys, array, Image
import os, string

# Load a data file and generate an image
def mkoverlay(filename, colours):
    incols = 994
    inrows = 1089
    img = Image.new('RGB', (incols,inrows))
    im = img.load()

    #im[99,99] = (0,0,0)
    # Read in the data
    f = file(filename)
    for y in range(inrows):
        row = array.array('h')
        row.fromfile( f, incols )
        row.byteswap()
        x = 0
        for v in row:
            im[x,y] = colours[v]
            x += 1
            pass
        pass
    return img

def read_clr(fname):
    colours = {}
    clrfile = file(fname, 'ra')
    for line in clrfile:
        entry = line.split()
        colours[int(entry[0])] = (int(entry[1]),int(entry[2]),int(entry[3]))
        pass
    return colours

if __name__ == "__main__":
    import sys
    inname = sys.argv[1]
    outname = inname.split('.')[0] + ".png"
    ctable = read_clr('rf.clr')
    img = mkoverlay(inname, ctable)
    img.save(outname)



