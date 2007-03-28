<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
   <head>
<title>Wepoco: Google map development</title>
<script src="http://maps.google.com/maps?file=api&v=2&key=ABQIAAAAF5oUqxaWkq3HzHxEjwFoMhSqLCR4vqZD7ui-J2nkp63kVD9LDRS75VKmRTRVCob68yw1NBkMXZHKsg" type="text/javascript"></script>
<script type="text/javascript" language="javascript">

var map = null;

function setupMap()
{

  map = new GMap2(document.getElementById("map"), 
		  {draggableCursor: 'crosshair'});
  map.addControl(new GLargeMapControl());
  map.addControl(new GScaleControl());

// ============================================================
// == We now have to write our own getTileUrl function ========

CustomGetTileUrl=function(a,b){
  // return "http://www.wepoco.com/maps/locate_box.png"
  return "http://www.wepoco.com/cgi/zoom.py?type=mpe&map="+"map"+"&x="+a.x+"&y="+a.y+"&zoom="+b
}
  
  
  var tilelayers = [
	G_NORMAL_MAP.getTileLayers()[0]
	,new GTileLayer(new GCopyrightCollection("Wepoco"),4,5)
	];
  var my_layer = 1;

tilelayers[my_layer].getTileUrl = CustomGetTileUrl;
tilelayers[my_layer].isPng = function() {return 1;}
// tilelayers[my_layer].getOpacity = function() {return 0.6;}

// I'm not sure if the following is still essential (ref. http://www.econym.demon.co.uk/googlemaps/custommap.htm )     
 tilelayers[my_layer].getCopyright = function(a,b) {
   return { prefix: "", copyrightTexts:["Wepoco"]};
 }
    
var custommap = new GMapType(tilelayers, G_SATELLITE_MAP.getProjection(), "Wepoco",
      {errorMessage:_mMapError});    

// == Add the maptype to the map ==
map.addMapType(custommap);
map.setCenter(new GLatLng(51.0, -4.0), 5, custommap);


GEvent.addListener(map, "click", 
		   function(marker, point) {
		     var info_div = document.getElementById('info');
		     el = document.createElement('p');
		     el.appendChild(document.createTextNode(point.lat().toFixed(4) + "N " + point.lng().toFixed(4) + "E"));
		     info_div.appendChild(el);
		   }
		   );

GEvent.addListener(map, "zoomend",
		   function(oldlev, newlev) {
		     var info_div = document.getElementById('info');
		     el = document.createElement('p');
		     el.appendChild(document.createTextNode("zoom="+newlev));
		     info_div.appendChild(el);
		   }
                   );
}

</script>

<style type="text/css">
.map-box {
   position: absolute;
   margin-left: 0px;
   margin-top: 50px;
   width: 630px;
   height: 380px;
   background-color: gray;
}

.map-info {
   position: absolute;
   overflow: auto;
   margin-left: 640px;
   margin-top: 50px;
   color: white;
   background-color: gray;
   width: 200px;
   height: 380px;
   font-family: courier;
   font-size: 12pt;
   color: black;
}


</style>

</head>

<body onload="setupMap()" onunload="GUnload()">
   <div id="map" class="map-box">
   </div>
<div id="info" class="map-info">
   <h4><a href="http://www.wepoco.com/">wepoco</a></h4>
</div>

<?php  readfile( 'analytics.html' ); ?>
</body>

</html>
