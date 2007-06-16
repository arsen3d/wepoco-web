<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Wepoco: Observations</title>
<link rel="stylesheet" href="/wepoco-look/banner.css" type="text/css" media="screen, projection" />
<link rel="stylesheet" href="observations.css" type="text/css" media="screen, projection" />

<script src="http://maps.google.com/maps?file=api&v=2&key=ABQIAAAAF5oUqxaWkq3HzHxEjwFoMhSqLCR4vqZD7ui-J2nkp63kVD9LDRS75VKmRTRVCob68yw1NBkMXZHKsg" type="text/javascript"></script>
<script type="text/javascript" src="observations.js"></script>
<script type="text/javascript" src="wCalendarDateInput.js">
/***********************************************
* A slightly modified (by Michael Saunby for Wepoco) version of the following -
*
* Jason's Date Input Calendar- By Jason Moon http://calendar.moonscript.com/dateinput.cfm
* Script featured on and available at http://www.dynamicdrive.com
* Keep this notice intact for use.
* 
* The modification is to call a function when the date is changed.
***********************************************/
/*
 * 24hr satellite rainfall estimates are generated at midnight so
 * set default date to yesterday.
 */
</script>
<script type="text/javascript">
yesterdate = new Date();
yesterdate.setDate(yesterdate.getDate()-1);
year = '' + yesterdate.getFullYear();
/* month is 0-11 !! */ 
month = '' + (yesterdate.getMonth() + 1);
if(month.length < 2){ month = '0' + month; }
date = '' +  (yesterdate.getDate());
if(date.length < 2){ date = '0' + date; }
var yesterday = year+month+date;
/* for NDVI use last month */
today =  new Date();
y = today.getFullYear();
m = today.getMonth();
if( m == 0){
  m = 12;
  y = y - 1;
}
year = '' + y;
month = '' + m;
if(month.length < 2){ month = '0' + month; }
var lastmonth = year+month+'01';


/*
 * There are several choices the user can make that affect the map
 * display.  Rather than use a callback from each input, this one is 
 * called for everything.
 */
function checkSelections()
{
  // Check type and date for each map layer that's enabled.
  var info = "";
  var raintype = null; var raindate = null;
  var ndvitype = null; var ndvidate = null;

  if(document.getElementById("ndvi_checkbox").checked){
    info = info + 'ndvi:on ';
    // Which product and date are required?
    ndvitype = document.getElementById("ndvitype").value;
    info = info + raintype + ' ';
    ndvidate = document.getElementById("ndvidate").value;
    info = info + raindate + ' ';
  }
  else{ ndvitype = null; }

  if(document.getElementById("rain_checkbox").checked){
    info = info + 'rain:on ';
    // Which product and date are required?
    raintype = document.getElementById("raintype").value;
    info = info + raintype + ' ';
    raindate = document.getElementById("raindate").value;
    info = info + raindate + ' ';
  }
  else{ raintype = null; }

  NdviAndRainLoad(ndvitype,ndvidate,raintype,raindate);
}

</script>
</head>
<body onload="checkSelections();setupNDVI();" onunload="saveLocation();GUnload()">
<div id="container">

<?php
  /* Setting $wepoco_selected highlight the link for this page.
   */
  $wepoco_selected = 'observations';

  include 'wepoco_header.php';
?>

<div>
<p>Rainfall estimates from Meteosat satellite observations. 
<a target="MPE_anim" href="http://oiswww.eumetsat.org/SDDI/cgi/listImages.pl?m=prod,sa=8,pr=MPEF,c=MPE">
View EUMETSAT MPE animation.</a></p>
</p>
</div>

<div style="position:relative;background:#FFFFFF;width:660px;height:580px;padding:20px;margin-top:0">

<div id="dateselect" class="calendar-left" style="margin:0" >
<form style="height:100%; padding: 0;" >
<table border="0" style="width:100%; height:100%; padding: 0"><tr>
  <td>
  <select id="ndvitype" onChange="checkSelections()">
  <option value="month">month NDVI</option>
  <option value="16day">16 day NDVI</option>
  </select>
  </td>
  <td>
<script>
  DateInput('ndvidate', true, 'YYYYMMDD', lastmonth)
  SetChangeFunc('ndvidate', 'checkSelections');
</script>
  </td>
  </tr>
  <tr>
  <td>
  <select id="raintype" onChange="checkSelections()">
  <option value="day">24hr rainfall</option>
  <option value="dekad">dekad rainfall</option>
  </select>
  </td>
  <td>
<script>
  DateInput('raindate', true, 'YYYYMMDD', yesterday);
  SetChangeFunc('raindate', 'checkSelections');
</script>
  </td>
  <td><img src="mpe_scale.gif" alt="MPE scale" /></td>
  </tr></table></form>
</div><!-- dateselect -->
<!-- the actual map -->
<div id="map" class="map-box" style="margin:0">
</div>

<div id="select" class="map-select" style="visibility:hidden" >
<input id="ndvi_checkbox" type="checkbox" checked="true" onClick="checkSelections()">NDVI</input><br/>
<input id="rain_checkbox" type="checkbox" checked="true" onClick="checkSelections()">Rainfall</input>
</div><!-- select -->

<?php  readfile( 'analytics.html' ); ?>

</div>

</div> <!-- container -->
</body>
</html>
