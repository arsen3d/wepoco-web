#!/bin/env python
# $Id$
#
# Michael Saunby. For Wepoco.
#
# $Author$
# $Date$


datadir='/home/mike/wepoco/data/mpe/'
mapdir = datadir + "map/"
lutdir = datadir + "lut/"
    
import os, Image, ImageDraw, cbdmap, metcoords
from gzip import GzipFile

def do_draw(img,map,proj,flip=(False,True)):
    (cols,rows) = img.size
    last_col = cols - 1
    last_row = rows - 1
    (flipx,flipy) = flip
    hdr = map.nexthdr()
    draw = ImageDraw.Draw(img)
    while hdr:
        (segid, maxlat, minlat, maxlong, minlong,
         rank, orglong, orglat, nstrokes) = hdr
        miss = 0
        try:
            (checkx,checky)=proj.fwd((maxlong,maxlat))
            if (checky < 1) or (checky > rows) or \
                   (checkx < 1) or (checkx > cols):
                miss += 1
                pass
            (checkx,checky)=proj.fwd((minlong,minlat))
            if (checky < 1) or (checky > rows) or \
                   (checkx < 1) or (checkx > cols):
                miss += 1
                pass
            (checkx,checky)=proj.fwd((minlong,maxlat))
            if (checky < 1) or (checky > rows) or \
                   (checkx < 1) or (checkx > cols):
                miss += 1
                pass
            (checkx,checky)=proj.fwd((maxlong,minlat))
            if (checky < 1) or (checky > rows) or \
                   (checkx < 1) or (checkx > cols):
                miss += 1
                pass
            pass
        except TypeError: # i.e. None returned by proj.fwd()
            miss = 4
            pass
        if miss == 4:
            hdr = map.nexthdr()
            continue
        (x,y) = proj.fwd((orglong,orglat))
        if flipx:
            x = last_col-x 
            pass
        if flipy:
            y = last_row-y
            pass
        last_pt = (x,y)
        pts = map.getpts()
        for i in range(0,len(pts),2):
            (x,y) = proj.fwd((pts[i],pts[i+1]))
            if flipx:
                x = last_col-x
                pass
            if flipy:
                y = last_row-y
                pass
            draw.line(last_pt + (x,y), fill=0)
            last_pt = (x,y)
            pass
        hdr = map.nexthdr()
        pass
    return

def proj4_map(projfn, dims):
    (width,height) = dims
    img = Image.new('L', dims, color=255)
    map = cbdmap.cbdfile(GzipFile("coast.bin.gz","rb"))
    do_draw(img,map,projfn)
    return img

# Google Maps projection
def google_proj(x, y, zoom, tile_size):
    proj="merc"
    lon_0=0.0
    lat_0=0.0
    to_meter= 156800 * pow(2,-zoom)

    y_0 = tile_size * to_meter * ((y+1)-(2**(zoom-1))) 
    x_0 = tile_size * to_meter * ((2**(zoom-1))-x)
    
    projfn = proj4.Projection(proj=proj,
                              lat_0=lat_0,
                              lon_0=lon_0,
                              to_meter=to_meter,
                              x_0=x_0, y_0=y_0)
    return projfn
    
def map_tile(destdir, x, y, zoom):
    tile_size = 256
    projfn = google_proj(x, y, zoom, tile_size)
    
    outwidth = tile_size
    outheight = tile_size
    img = proj4_map(projfn,(outwidth, outheight))
    tilename = "%d/%d_%d.png" % (zoom, x, y)
    img.save( destdir + tilename )

def reproj_msat_lut(destdir, x, y, zoom):
    import metcoords, array
    tile_size = 256
    projfn = google_proj(x, y, zoom, tile_size)
    outwidth = tile_size
    outheight = tile_size
    met_fwd = metcoords.Meteosat(size=2500,generation=1).fwd
    met_rows = 2500
    met_cols = 2500
    matrix = array.array('h') # Short ints (half-words)
    for row in range(outheight):
        for col in range(outwidth):
            lonlat = projfn.inv((col,(outheight-1)-row))
            try:
                (msatx,msaty) = met_fwd(lonlat)
                matrix.append((met_cols-1)-int(msatx))
                matrix.append((met_rows-1)-int(msaty))
            except:
                matrix.append(0)
                matrix.append(0)
            pass
        pass
    matrixname = "%d/%d_%d.msat_lut" % (zoom, x, y)
    f = file(destdir + matrixname,'wb')
    matrix.tofile(f)
    f.close()

def reproj_msg_lut(destdir, x, y, zoom):
    import metcoords, array
    tile_size = 256
    projfn = google_proj(x, y, zoom, tile_size)
    outwidth = tile_size
    outheight = tile_size
    met_fwd = metcoords.Meteosat(size=3712,generation=2).fwd
    met_rows = 3712
    met_cols = 3712
    matrix = array.array('h') # Short ints (half-words)
    for row in range(outheight):
        for col in range(outwidth):
            lonlat = projfn.inv((col,(outheight-1)-row))
            try:
                (msatx,msaty) = met_fwd(lonlat)
                matrix.append((met_cols-1)-int(msatx))
                matrix.append((met_rows-1)-int(msaty))
            except:
                matrix.append(0)
                matrix.append(0)
            pass
        pass
    matrixname = "%d/%d_%d.msg_lut" % (zoom, x, y)
    f = file(destdir + matrixname,'wb')
    matrix.tofile(f)
    f.close()

def prepare_tiles( zoom, x_min, y_min, x_max, y_max ):
    try:
        #os.mkdir( mapdir + "%d" % (zoom) )
        os.mkdir( lutdir + "%d" % (zoom) )
    except:
        print "dirs exist"
        pass
    for y in range(y_min,y_max):
        for x in range(x_min,x_max):
            print "generating map and lut for", x, y, zoom
            #map_tile( mapdir, x, y, zoom )
            reproj_msg_lut( lutdir, x, y, zoom )
            pass
        pass
    return
    
if __name__ == "__main__":
    import proj4

    try:
        #os.mkdir( mapdir )
        os.mkdir( lutdir )
    except:
        print "dirs exist"
        pass
    
    prepare_tiles(zoom=2, x_min=1, y_min=1, x_max=3, y_max=3 )
    prepare_tiles(zoom=3, x_min=3, y_min=3, x_max=6, y_max=5 )
    prepare_tiles(zoom=4, x_min=7, y_min=6, x_max=11, y_max=10 )
    prepare_tiles(zoom=5, x_min=14, y_min=12, x_max=21, y_max=20 )

