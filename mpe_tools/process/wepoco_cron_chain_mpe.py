#!/usr/bin/python
#
# This is a cron 'chain' script for wepoco processing of Eumetsat
# 'MPE' precipitation estimates.
#
# Chain scripts execute a chain of python scripts.  
# chain() checks for success or failure of a command. On failure the chain
# aborts.

WEPOCO_HOME = '/home/mike/wepoco/'
WEPOCO_BIN = WEPOCO_HOME + 'bin/'
WEPOCO_LOG = WEPOCO_HOME + 'log/'

CHAIN_LOG = WEPOCO_LOG + 'chain_mpe-log'

#
# These two functions make the chain work.
#
import sys

def log( logname, item, msg):
    import time
    log = file(logname, 'a+')
    log.write(time.asctime() + ':' + item + ':' + msg + '\n')
    log.close()
    return

def chain( item ):
    try:
        exec 'import ' + item
        exec '(code, msg) = ' + item + '.run()'
    except:
        log( CHAIN_LOG, item, 'exec failed')
        sys.exit(0)
    if code:
        log( CHAIN_LOG, item, msg)
        sys.exit(0)
    else:
        log( CHAIN_LOG, item, 'OK')
        pass
    return

####################################################

chain( 'fetch_eumetsat_mpe' )
chain( 'accumulate_mpe' )
# The png_generation only happens at the end of the daily accumulation
# So failure is expected - to break the chain.
chain( 'png_from_mpe' )
chain( 'map_tiles_mpe' )
#chain( 'map_overlay_mpe' )
chain( 'upload_daily_mpe' )
chain( 'upload_daily2_mpe' )
# chain( 'tidy_mpe' )
# Accumulate daily files to generate dekad and month accumulations
chain( 'acc_dek_mpe' )
