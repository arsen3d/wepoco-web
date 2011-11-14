#!/usr/bin/python
#
# Tell me about a CSV file.
#
# The sniffer dialect does understand more than this,
# but it's all I need for now. 

import sys,csv

def main():
    argv=sys.argv
    try:
        infile = open(argv[1], 'rb')
    except:
        print >>sys.stderr, "ERROR.  Usage is:"
        print >>sys.stderr, "%s infile.csv" % argv[0] 
        return 1

    dialect = csv.Sniffer().sniff(infile.read(2048))

    d = ord(dialect.delimiter)
    if d == 9:
        delimiter = "<tab>"
    elif d > 32 and d < 127:
        delimiter = dialect.delimiter
    else:
        delimiter = "<Hex:%X>" % d
        pass
    print "delimiter is", delimiter
    print "quotechar is", dialect.quotechar
    print "quoting is", dialect.quoting
    if dialect.escapechar != None:
        print "escapechar is", dialect.escapechar
    return 0

if __name__ == '__main__':
  sys.exit(main())
