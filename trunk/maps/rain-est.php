<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
   <head>
<title>Wepoco: Africa rainfall estimate</title>
<script src="http://maps.google.com/maps?file=api&v=2&key=ABQIAAAAF5oUqxaWkq3HzHxEjwFoMhSqLCR4vqZD7ui-J2nkp63kVD9LDRS75VKmRTRVCob68yw1NBkMXZHKsg" type="text/javascript"></script>
<script type="text/javascript" language="javascript" src="markers.js"></script>
<script type="text/javascript" language="javascript" src="rain-est.js"></script>
<style type="text/css"> @import url("wepoco.css"); </style>
</head>
<body onload="setupMPE()" onunload="GUnload()">
   <div id="map" class="map-box">
   </div>
<div id="heading" class="heading">
   <h2>rainfall estimate:</h2>
</div>
<div id="scale" class="map-scale">
   <?php readfile( 'scale.html' ); ?>
</div>
<div id="info" class="map-info">
   <h4><a href="http://www.wepoco.com/">wepoco</a></h4></div>
<div id="timeline" class="timeline">
   <?php  readfile( 'mpe/timelinedek.html' ); ?>
   <?php  readfile( 'mpe/timelineday.html' ); ?>
</div>
<?php  readfile( 'analytics.html' ); ?>
</body>
</html>
