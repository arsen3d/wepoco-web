#!/usr/bin/python
#
# Simple translation of plain text monthly weather summaries to CSV
#
# The input files can be obtained here http://www.metoffice.gov.uk/hadobs/crutem3
# These data are derived from CLIMAT reports.
# 

import sys,csv, re

class wmoDialect(csv.Dialect):
    delimiter = '\t'
    quotechar = '"'
    quoting = 0
    lineterminator = '\n'

def main():
    argv=sys.argv
    try:
        reader = csv.DictReader(open(argv[1], 'rb'), dialect=wmoDialect)
        writer = csv.writer(open(argv[2], 'wb'), quoting=csv.QUOTE_ALL)
    except:
        print >>sys.stderr, "ERROR.  Usage is:"
        print >>sys.stderr, "%s infile.flatfile outfile.csv" % argv[0] 
        return 1
    writer.writerow(['IndexNbr','IndexSubNbr','LatLng','StationName','RegionId',
                  'RegionName','CountryArea','CountryCode','StationId'])
    for row in reader:
        try:
            lat = re.match("(\d\d) (\d\d) (\d\d)([N|S])",row['Latitude']).groups()
            lng = re.match("(\d+) (\d\d) (\d\d)([E|W])",row['Longitude']).groups()
            latf = float(lat[0]) + float(lat[1])/60 + float(lat[2])/3600
            if lat[3] == 'S': latf = -latf 
            lngf = float(lng[0]) + float(lng[1])/60 + float(lng[2])/3600
            if lng[3] == 'W': lngf = -lngf
            latlng = "%.2f,%.2f" % (latf,lngf)
        except:
            latlng = None
            pass
        outrow = [row['IndexNbr'],row['IndexSubNbr'],latlng,row['StationName'],row['RegionId'],
                  row['RegionName'],row['CountryArea'],row['CountryCode'],row['StationId']]
        writer.writerow(outrow)
    return 0

if __name__ == '__main__':
  sys.exit(main())
