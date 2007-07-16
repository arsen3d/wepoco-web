Proj4 interface for Python
--------------------------

Author: mike@saunby.net
$Date$
$Id$

0. Before installing
--------------------

What this software does :- 

 It's an interface to the Proj4 cartographic library for Python programmers.
You can use it to convert latitudes and longitudes to x,y coordinates in 
many different projections. I've used it to convert between the view of
earth from geostationary weather satellites to some of the projections used
for weather charts and forecaster display systems.

What else will you need :-

 * Python   see http://www.python.org
 
 * Proj4 see http://www.remotesensing.org/proj (The documentation is quite long and complicated.  You will need to read the first part of OF90-284.pdf to get an idea of what Proj is and how to use it)

 * Something to use it for. This software is only an interface, you'll need to write your own application, but there should be at least one example in the examples directory.

1. Installing
-------------

 "python setup.py install" should be all you need to do.  If it doesn't work then you'll need to take a look at setup.py and perhaps change the paths to the
proj library and include file.  If that doesn't work try the Python documentation for the distutils package - which is how setup.py does its stuff.

2. Try it
---------

 The examples won't work until the interface is installed.

 