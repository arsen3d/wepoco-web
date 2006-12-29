##############################################################################  

import sys, shutil, array, Image

# Copy from src file to dst file translating 9999.0 to 0.0
def copy_data( srcf, dstf ):
    eof = False
    while eof == False:
        data = array.array( 'd' )
        # 'fromfile' raises EOFError at end of file
        try:
            data.fromfile( srcf, 1024 )
        except EOFError:
            eof = True
            pass        
        idx = 0
        for x in data:
            if x == 9999.0:
                data[idx] =  0.0
            idx = idx + 1
            pass
        data.tofile( dstf )
        pass
    return
    
def add_incr( sumf, incrf, tmpf ):
    eof = False
    while eof == False:
        sumbuf = array.array( 'd' )
        data = array.array( 'd' )
        # 'fromfile' raises EOFError at end of file
        try:
            sumbuf.fromfile( sumf, 1024 )
        except EOFError:
            eof = True
            pass
        try:
            data.fromfile( incrf, 1024 )
        except EOFError:
            pass
        
        idx = 0
        for x in data:
            if x !=  9999.0:
                sumbuf[idx] =  sumbuf[idx] + x
                pass
            idx = idx + 1
            pass
        
        sumbuf.tofile( tmpf )
        pass
    return

    
if __name__ == "__main__":

    sumname = sys.argv[1]
    incname = sys.argv[2]

    try:
        incfile = file( incname, 'rb' )
    except:
        print "file", incname, "does not exist or cannot be opened"
        sys.exit( 1 )

    try:
        sumfile = file( sumname, 'rb' )
    except:
        # Assume that we are to start a new total
        sumfile = file( sumname, 'wb' )
        print "copying", incname, "to", sumname
        copy_data( incfile, sumfile )
        sys.exit( 0 )
        pass

    print "adding newfile to sumfile"
    try:
        newfile = file( sumname + '~', 'wb' )
    except:
        print "file", sumname + '~', "cannot be opened"
        sys.exit( 1 )
        pass

    add_incr( sumfile, incfile, newfile )

    newfile.close()
    sumfile.close()
    incfile.close() 
    
    shutil.move( sumname + '~', sumname )
    
    sys.exit( 0 )
    
##############################################################################  
