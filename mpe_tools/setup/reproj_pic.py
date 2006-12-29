#!/usr/bin/python
#
# reproj_pic.py
#

import sys, Image, array

if __name__ == "__main__":

    inpic = Image.open(sys.argv[2])
    (inrows,incols) = inpic.size

    outrows = 256
    outcols = 256

    if incols == 2500:
        proj = "msat"
    elif incols == 2300:
        proj = "msat"  # "trimmed" meteosat
    elif incols == 3712:
        proj = "msg"
    else:
        print "Can't figure out what to do."
        print "Input image is neither 2500x2500 nor 3712x3712"
        pass
    
    matrix = array.array('h')
    matrix.fromfile(file(sys.argv[1],'rb'),outrows*outcols*2)

    outpic = Image.new(inpic.mode,(outcols,outrows))

    for y in range(outrows):
        for x in range(outcols):
            xmsat = matrix[y*outcols*2 + x*2]
            ymsat = matrix[y*outcols*2 + x*2 +1]
            if incols == 2300:
                xmsat = xmsat - 100
                ymsat = ymsat - 100
                pass
            try:
                p = inpic.getpixel((xmsat,ymsat))
                outpic.putpixel((x,y), p)
            except:
                pass
            pass
        pass
    
    outpic.save(sys.argv[3])

