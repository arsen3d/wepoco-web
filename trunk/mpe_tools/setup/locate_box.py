#!/bin/env python
#
import Image, ImageDraw

if __name__ == "__main__":

    tilesize = 256
    img = Image.new('L', (tilesize,tilesize), color=0)
    draw = ImageDraw.Draw(img)
    draw.line((0,0) + (0,256), fill=1)
    draw.line((0,0) + (256,0), fill=1)
    img.save("locate_box.png", transparency=0)



