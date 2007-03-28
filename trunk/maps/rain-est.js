// rain-est.js
// Michael Saunby.  For Wepoco.
//

var selected_map = "latest";
var custommap;
var map;


function printToDiv( divname, text )
{
  var div = document.getElementById( divname );
  div.innerHTML = text;
}

function MPEidToDate( id )
{
  if(id.substr(11,3) == 'DEK'){
   return "dekad "  + id.substr(14,1)
  }else{
    return id.substr(4,4) + '-' + id.substr(8,2) + '-' + id.substr(10,2);
  }
}

function selectMap( but )
{
  // reset all buttons to default style
  var timeline_div = document.getElementById( "timeline"  ); 
  var buttons = timeline_div.getElementsByTagName( 'button' );
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].style.color = "black";
    buttons[i].style.fontWeight = "normal";
  }
  // mark selected button
  but.style.color = "#CC0000";
  but.style.fontWeight = "bold";
  
  // What we're here for - change the map selection
  selected_map = but.id;
  // I can't believe it's as simple as this - but it works. 
  map.setMapType(custommap);
  document.getElementById("map").style.backgroundColor = "#000000";

  // Other stuff
  text = MPEidToDate( but.id );
  // printToDiv( "info", "<p>" + text + "</p>" );
  printToDiv( "heading", "<h2>rainfall estimate: " + text + "</h2>" );
  
  return;
}
    
function setupMPE()
{

map = new GMap2(document.getElementById("map"));
map.addControl(new GLargeMapControl());
map.addControl(new GScaleControl());

// ============================================================
// == We now have to write our own getTileUrl function ========

CustomGetTileUrl=function(a,b){
  return "http://www.wepoco.com/tiles/tile.py?map="+selected_map+"&x="+a.x+"&y="+a.y+"&zoom="+b
  // This works too, but can't handle missing tiles
  //return "http://www.wepoco.com/maps/mpe/"+selected_map+"/"+b+"/"+a.x+"_"+a.y+".png"
}
  
  
// ============================================================
// ====== Create a single layer "Rain rate" custom maptype ====== 
//
// == Create the GTileLayer ==
//  var tilelayers = [
//	new GTileLayer(new GCopyrightCollection("Meteorological data: Wepoco"),4,5)
//	,G_HYBRID_MAP.getTileLayers()[1]
//	];
//  var rain_idx = 0;
  var tilelayers = [
	G_NORMAL_MAP.getTileLayers()[0]
	,new GTileLayer(new GCopyrightCollection("Meteorological data: Wepoco"),4,5)
	,G_HYBRID_MAP.getTileLayers()[1]
	];
  var rain_idx = 1;


// // Or without map - 
//  var tilelayers = [
//  new GTileLayer(new GCopyrightCollection("Meteorological data: Wepoco"),4,5)
//  ];     
tilelayers[rain_idx].getTileUrl = CustomGetTileUrl;
tilelayers[rain_idx].isPng = function() {return 1;}
tilelayers[0].getOpacity = function() {return 0.6;}

// I'm not sure if the following is still essential (ref. http://www.econym.demon.co.uk/googlemaps/custommap.htm )     
  tilelayers[rain_idx].getCopyright = function(a,b) {
    return { prefix: "Meteorological Data:", copyrightTexts:["Wepoco"]};
  }
    
// == Create the GMapType, copying most things from G_SATELLITE_MAP ==
var custommap = new GMapType(tilelayers, G_SATELLITE_MAP.getProjection(), "Rain rate",
      {maxResolution:5,minResolution:3,errorMessage:_mMapError});    

// == Add the maptype to the map ==
map.addMapType(custommap);
//map.setCenter(new GLatLng(13.44, 35.93), 4, custommap);
map.setCenter(new GLatLng(10.0, 16.0), 3, custommap);


GEvent.addListener(map, "click", 
		   function(marker, point) {
		     var info_div = document.getElementById('info');
		     el = document.createElement('p');
		     el.appendChild(document.createTextNode(point.lat().toFixed(3) + "N " + point.lng().toFixed(3) + "E"));
		     info_div.appendChild(el);
		   }
		   );

var info_div = document.getElementById( "info"  );
info_div.innerHTML = "<p>" + initial_selection + "</p>";

var but = document.getElementById(  initial_selection  );
selectMap( but );
showMarkers( map );
}
