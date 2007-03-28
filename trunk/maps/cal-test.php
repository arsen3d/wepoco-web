<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
   <head>
<title>Wepoco: NDVI demo</title>
<script type="text/javascript" src="calendarDateInput.js">
/***********************************************
* Jason's Date Input Calendar- By Jason Moon http://calendar.moonscript.com/dateinput.cfm
* Script featured on and available at http://www.dynamicdrive.com
* Keep this notice intact for use.
***********************************************/
</script>

<style type="text/css"> @import url("wepoco_a.css"); </style>
</head>
<body>

<div id="banner" class="banner">
   <?php readfile( 'obsbanner.html' ); ?>
</div>

<div id="map" class="map-box"></div>

<div id="heading" class="heading">
   <h2>NDVI</h2>
</div>
<div id="scale" class="map-scale">
   <?php readfile( 'scale.html' ); ?>
</div>

<div id="info" class="map-info">
   <h4><a href="http://www.wepoco.com/">wepoco</a></h4>
</div>

<div id="dateselect" class="calendar">
<form>
<table border="0">
  <tr>
  <td>
  <input type="button" onClick="alert('MPE_' + this.form.orderdate.value + '_M8_00')" value="24hr rainfall" />
  </td>
  <td>
  <script>DateInput('orderdate', true, 'YYYYMMDD')</script>
  </td>
  </tr>
</table>
</form>
</div>

</body>
</html>
