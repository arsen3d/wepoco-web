#!/bin/bash

loc=lat=13.28\&lng=105.88
yrs=yr0=2007\&yr1=2007
pars="soilm prate runoff air.2m"

for par in $pars; do
 python gviz20cr.py ${loc}\&fi=${par}\&tqx=out:csv\&${yrs}\&mo0=1\&mo1=12 >${par}_cam2007.csv
done
