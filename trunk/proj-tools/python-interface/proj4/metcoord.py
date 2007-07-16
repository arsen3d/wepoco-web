#!/usr/bin/env python
#
# metcoord.py
# Convert latitude-longitude to coordinate system used for the
# Meteosat geostationary weather satellites operated by Eumetsat.
# See http://www.eumetsat.de for more information on these satellites.
#
# Michael Saunby
# mike@saunby.net
#
# $Date$
# $Id$

import proj4
import readline
import string
from math import radians, degrees

# Radius of (spherical) earth
re=6370.997
# If an ellipsoid were allowed this is what Eumetsat use: re=6378.155 rf=297.0

# Orbit height of geostationary satellite
hght=35785.845
# All geostationary satellites are at 0 degrees north.
# The nominal position for the primary European satellite
# is 0 degrees east (Greenwhich meridian). 
meteosat_lon=0.0
msg_lon=0.0
# Scale factors for geostationary weather satellites. These
# are related to the pixel size (or more coorectly scan a
# To caluculate them the easiest thing to do is set x_0 and y_0 to 0.0
# and use a scale of 1.0 (i.e. a = re) then get the value for 80 degrees N
# at the same longitude as the satellite (0 E for Meteosat).
# If that doesn't make sense, then draw yourself a diagram and figure it out
# from there.
# Note that Proj4 assumes a sphere, not an ellipsoid for this projection so there
# will be very slight errors (a maximum of 1.5 pixels for Meteosat) compared with the
# Eumetsat supplied algorithm. This means that in most cases the correct, or adjacent
# pixel is located, which is fine for map overlays, etc.
#
meteosat_scale=4.539
msg_scale="DON'T KNOW"
meteosat_x_0=1250.5
meteosat_y_0=1250.5


proj = proj4.Projection(proj="nsper",
           lat_0=0.0, lon_0=meteosat_lon,
           a=re/meteosat_scale,
           h=hght/meteosat_scale,
           x_0=meteosat_x_0, y_0=meteosat_y_0)

print "Enter (in degrees) lon, lat:"
intxt = raw_input()
while len(intxt):
    inp = string.split(intxt) 
    lon = radians(float(inp[0]))
    lat = radians(float(inp[1]))
    (y,x) = proj.fwd((lon,lat))
    (lon, lat) = proj.inv((y,x))
    print "(y, x) = ", y, x, " inverse: ", degrees(lon), degrees(lat)
    print
    print "Enter (in degrees) lon, lat:"
    intxt = raw_input()


