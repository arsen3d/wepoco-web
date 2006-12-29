#!/usr/bin/python
# Michael Saunby. For Wepoco.
# $Date$
#
##############################################################################

import string

sat_id = 'M8'  # Meteosat 8
    
month_names = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    
def dek_name( (year, month, start_day) ):
    dek_names = {}
    dek_names[1] = "1"
    dek_names[11] = "2"
    dek_names[21] = "3"
    label = month_names[month-1] + ' dekad ' + dek_names[start_day]
    id = "MPE_%4d%02d_DEK%s" % (year, month, dek_names[start_day])
    return """
<td><button id="%s" onClick="selectMap(this)">%s</button></td>""" % (id, label)

def dek_set( year, month, day):
    if month == 1:
        month_p = 12
        year_p = year - 1
    else:
        month_p = month - 1
        year_p = year
        pass
    text = ""
    if day > 20:
        dekad_c = (year, month, 11)
        dekad_b = (year, month, 1)
        dekad_a = (year_p, month_p, 21)
    elif day > 10:
        dekad_c = (year, month, 1)
        dekad_b = (year_p, month_p, 21)
        dekad_a = (year_p, month_p, 11)
    else:
        dekad_c = (year_p, month_p, 21)
        dekad_b = (year_p, month_p, 11)
        dekad_a = (year_p, month_p, 1) 
        pass
    for dek in [dekad_a, dekad_b, dekad_c]:
        text = text + dek_name( dek ) + '\n'
        pass
    return text

def day_name( ( year, month, day ) , disabled ):
    id = "MPE_%4d%02d%02d_%s_00" % (year, month, day, sat_id)    
    if disabled:
        return """
<td><button id="%s" disabled="true">%02d</button></td>""" % (id, day)
    else:
        return """
<td><button id="%s" onClick="selectMap(this)">%02d</button></td>""" % (id, day)

def day_set( year, month, day ):
    days = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    # No way will this code be used in 2100 - when the following rule breaks.
    if (year%4) == 0:
        days[2] = 29
        pass
    if day > 21:
        start = 11
        end = days[month]
    elif day > 11:
        start = 1
        end = 20
    else:
        # ideally I'd like to start with the previous month
        # but it's easier to add this comment for now.
        start = 1
        end = 20
        pass
    text = ""
    for d in range(start,day+1):
        text = text + day_name( (year, month, d), False ) + '\n'
        pass
    for d in range(day+1,end+1):
        text = text + day_name( (year, month, d), True ) + '\n'
        pass
    return (end-start+1, text)
        

def mk_timeline_orig( datadir=None, sumname=None ):

    year = int(sumname[4:8])
    month = int(sumname[8:10])
    day = int(sumname[10:12])
    sat_id = sumname[13:15]
    timeline_file = file( datadir + "timeline.html", 'wb' )

    timeline_text = """
<table border="0">
<caption></caption>
<tbody>
<tr>"""
    text = dek_set( year, month, day )
    timeline_text = timeline_text + text
    (ndays, text) = day_set( year, month, day )
    timeline_text = timeline_text + text 
    timeline_text = timeline_text + """
</tr>
<tr>
<td colspan="3">
<div style="text-align: center; background-color: white">&nbsp;&nbsp;</div>
</td>
<td colspan="%d">
<div style="text-align: center; background-color: gray">&nbsp;%s %d&nbsp;</div>
</tr>
</tbody>
</table>
<script type="text/javascript" language="javascript">
 var initial_selection="MPE_%4d%02d%02d_%s_00";
</script>
""" % (ndays, month_names[month-1], year,year,month,day, sat_id)
    timeline_file.write( timeline_text )
    timeline_file.close()
    return

def mk_timeline( datadir=None, sumname=None ):
    year = int(sumname[4:8])
    month = int(sumname[8:10])
    day = int(sumname[10:12])
    sat_id = sumname[13:15]
    timeline_file = file( datadir + "timelinedek.html", 'wb' )
    timeline_text = """
<table border="0">
<caption></caption>
<tbody>
<tr>"""
    text = dek_set( year, month, day )
    timeline_text = timeline_text + text
    timeline_text = timeline_text + """
</tr>
</tbody>
</table>
"""
    timeline_file.write( timeline_text )
    timeline_file.close()

    timeline_file = file( datadir + "timelineday.html", 'wb' )
    timeline_text = """
<table border="0">
<caption></caption>
<tbody>
<tr>"""
    (ndays, text) = day_set( year, month, day )
    timeline_text = timeline_text + text
    timeline_text = timeline_text + """
</tr>
</tbody>
</table>
<script type="text/javascript" language="javascript">
 var initial_selection="MPE_%4d%02d%02d_%s_00";
</script>
""" % (year,month,day, sat_id)

    timeline_file.write( timeline_text )
    timeline_file.close()
    return

def run():
    datadir='/home/mike/wepoco/data/mpe/'
    config = 'acc.out'
    try:
        configf = file( datadir + config, 'r' )
        discard = string.strip( configf.readline() )
        sumname = string.strip( configf.readline() )
        lasttmp = string.strip( configf.readline() )
        configf.close()
    except Exception, inst:
        # print inst
        return (1, 'Failed to read configuration file')

    mk_timeline_orig( datadir=datadir, sumname=sumname )
    mk_timeline( datadir=datadir, sumname=sumname )
    return (0, 'OK')

if __name__ == "__main__":
    import sys
    force = True
    (rc, msg) = run()
    print msg
    sys.exit( rc )
