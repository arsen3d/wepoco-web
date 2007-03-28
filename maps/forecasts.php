<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Wepoco: Forecasts</title>
<link rel="stylesheet" href="/wepoco-look/banner.css" type="text/css" media="screen, projection" />
<link rel="stylesheet" href="forecasts.css" type="text/css" media="screen, projection" />
<script src="http://maps.google.com/maps?file=api&v=2&key=ABQIAAAAF5oUqxaWkq3HzHxEjwFoMhSqLCR4vqZD7ui-J2nkp63kVD9LDRS75VKmRTRVCob68yw1NBkMXZHKsg" type="text/javascript"></script>
<script type="text/javascript" src="forecasts.js"></script>
<script type="text/javascript" src="cookies.js"></script>
<script type="text/javascript" src="markers.js"></script>

</head>
<body onload="SetupMap()" onunload="saveLocation(map);GUnload()">
<div id="container">
<?php
  /* Setting $wepoco_selected highlight the link for this page.
   */
  $wepoco_selected = 'forecasts';

  include 'wepoco_header.php';
?>
<div>
<p>Experimental weather forecasts based on
<a href="http://www.emc.ncep.noaa.gov/gmb/ens/">NCEP ensembles</a>.
There's much more planned for this page, so please come back soon.
</p>
</div>
<div style="position:relative;background:#FFFFFF;width:660px;height:600px;padding:20px;margin-top:0">
<!-- the actual map -->
<div id="map" class="map-box" ></div>

<?php  include( 'analytics.html' ); ?>

</div>

</div> <!-- container -->
</body>
</html>
