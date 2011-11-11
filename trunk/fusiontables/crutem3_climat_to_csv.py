#!/usr/bin/python
#
# Simple translation of plain text monthly weather summaries to CSV
#
# The input files can be obtained here http://www.metoffice.gov.uk/hadobs/crutem3
# These data are derived from CLIMAT reports.
# 

import sys,csv, re

# replace any missing values with None
def replace_missing(ar,missing):
    while True:
        try:
            # if index() fails there are no more missing values
            ar[ar.index(missing)]=None
        except:
            return ar
        pass
    pass

# apply scaling factor of 0.1 to values in tenths
def rescale(ar,indexes):
    for i in indexes:
        if ar[i] != None: 
            ar[i] = int(ar[i]) * 0.1 
            pass
        pass
    return ar

def main():
    argv=sys.argv
    try:
        infile = open(argv[1], 'r')
        writer = csv.writer(open(argv[2], 'wb'), quoting=csv.QUOTE_ALL)
    except:
        print >>sys.stderr, "ERROR.  Usage is:"
        print >>sys.stderr, "%s infile.txt outfile.csv" % argv[0] 
        return 1
    hdr = infile.next()
    try:
        mch = re.search("'CLIMAT' DATA FOR\ +(\d\d\d\d/\d\d).*", hdr)
        date = mch.group(1)
    except:
        print >>sys.stderr, "ERROR: Input format error"
        return 1
    for n in range(5): infile.next()
    for row in infile:
        a = row.split()
        a = replace_missing(a,'-32768')
        a = rescale(a, [2,3,4,5,11,12])
        a.insert(0,date)
        writer.writerow(a)
    return 0

if __name__ == '__main__':
  sys.exit(main())
