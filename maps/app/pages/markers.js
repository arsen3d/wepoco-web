
var ncep_url = "http://home.badc.rl.ac.uk/astephens/ncep_data/";

var urlbase="http://home.badc.rl.ac.uk/astephens/ncep_data/";

var legend_body = '<img src="plot_legend.gif" />';
//var plot_style = "margin-top:-45px;margin-left:-20px;position:absolute;clip:rect(45px 380px 340px 20px)";
var plot_style = "";

function padInt(intValue, padLength) {
    // pads out int string
    var s=intValue.toString();
    while (s.length<padLength) {
        s="0"+s;
    }
    return s;
}

function getLatestDate(offset) {
    // gets Latest date as 8 char string
    var today=new Date();
    if (offset!=0) {
        today.setDate(today.getDate()+offset);
    }
    var year=today.getFullYear().toString();
    var month=padInt(today.getMonth()+1, 2);
    var day=padInt(today.getDate(), 2);
    var today=year+month+day;
    return today;
}

function getLatestURL(location) {
    // Returns the URL for latest date and location selected 

    var today=new Date();
    var hour=today.getHours();
    if (hour<10) { // use yesterday
        today=getLatestDate(-1);
    } else {
        today=getLatestDate(0);
    }
    var datetime=today+"00";
    var url=urlbase+datetime+"_"+location+"_rainfall.gif";
    return url;
}



function closeInfoWindow() {
  map.setCenter( map.lastPageCenter, map.lastPageZoom );
  // but might need recenter_point = map.getCenterLatLng();
}


function createMarker( point, location_name, id ) {
   var marker = new GMarker( point, {title:location_name} );

// was width:360px;height:295px
   var tab_body =  '<div style="width:250px;height:240px" class="info-window"><img style="'+plot_style+
	 '" src="' + 	getLatestURL( id )  + '" /></div>';

   var tabs = [
	new GInfoWindowTab( location_name, tab_body ),
        new GInfoWindowTab( 'legend', legend_body )
	];
   GEvent.addListener(marker, "click", function() {
	map.savePosition();
        marker.openInfoWindowTabsHtml( tabs );
      });
  GEvent.addListener(marker, "infowindowclose", function() {
	map.returnToSavedPosition();
      });

   return marker;
}



function showMarkers( map ) {
  prepareMarkers( map );
  zoom = map.getZoom();
}

function prepareMarkers( map ){
  mgr = new GMarkerManager( map );
  var  markers_lev3 = [];
  var  markers_lev4 = [];
  var  markers_lev5 = [];
  GDownloadUrl("ethiopia.xml", function(data, responseCode) {
    var xml = GXml.parse(data);
    var markers = xml.documentElement.getElementsByTagName("marker");
    for (var i = 0; i < markers.length; i++) {
      var point = new GLatLng(parseFloat(markers[i].getAttribute("lat")),
                            parseFloat(markers[i].getAttribute("lng")));
      var text = markers[i].getAttribute("label"); 
      var id =  markers[i].getAttribute("id");
      var level = parseInt( markers[i].getAttribute("level") );
      mark =  createMarker(point, text, id);
      if (level == 3) markers_lev3.push( mark );
      if (level == 4) markers_lev4.push( mark );
      if (level == 5) markers_lev5.push( mark );
    }
    // Important that this is done here (inside callback) as GDownloadUrl makes
    // async call.
    mgr.addMarkers( markers_lev3, 3 );
    mgr.addMarkers( markers_lev4, 4 );
    mgr.addMarkers( markers_lev5, 5 );
    mgr.refresh();
  });
}

function redrawMarkers( map, zoom ) {
  //
}


