// observations-dev.js
// Michael Saunby.  For Wepoco.
//

var selected_rain = "none";
var selected_raindate = "none";
var selected_ndvi = "none";
var ndvimap, rainmap, bothmap, currentmap;
var map = null;
var tilesite = "/tileget/";
//var tilesite = "http://wepoco.s3.amazonaws.com/mpe/";

function getCookie(c_name)
{
    if (document.cookie.length>0)
	{
	    c_start=document.cookie.indexOf(c_name + "=")
		if (c_start!=-1)
		    { 
			c_start=c_start + c_name.length+1;
			c_end=document.cookie.indexOf(";",c_start);
			if (c_end==-1) c_end=document.cookie.length;
			return unescape(document.cookie.substring(c_start,c_end));
		    } 
	}
    return null;
}

function setCookie(c_name,value,expiredays)
{
    var exdate=new Date();
    exdate.setDate(exdate.getDate()+expiredays);
    document.cookie=c_name+ "=" +escape(value)+
	((expiredays==null) ? "" : ";expires="+exdate);
}

/*
 * Store a cookie with present map centre and zoom level.
 * If user returns within x days these values will be used
 * rather than default.
 */
function saveLocation() {
    centre = map.getCenter();
    lat=centre.lat();
    lng=centre.lng();
    loc = "" + lat + "," + lng;
    setCookie( "WepocoLatLng", loc, 20 );
    zoom = map.getZoom();
    setCookie( "WepocoZoom", "" + zoom, 20 );
    return;
}

function getSavedLocation() {
    centre = getCookie( "WepocoLatLng" );
    zoom = getCookie( "WepocoZoom" );
    if (centre === null){
	return null;
    }else{
	ll = centre.split(",");
        if(zoom == null){ zoom = 3; }  // unlikely, but possible. 
	return [Number(ll[0]), Number(ll[1]), Number(zoom)];
    }
}

function setRainType( value ){
    rain_type = value;
    return;
}

function NdviAndRainSelect( ndvitype, raintype ){
    if( ndvitype && raintype ){
	currentmap =  bothmap;
    }
    else if( (ndvitype==null) && raintype ){
	currentmap = rainmap;
    }
    else if( ndvitype && (raintype==null) ){
	currentmap = ndvimap;
    }
    else{
	currentmap = ndvimap;
    }
    return;
}

function NdviAndRainLoad( ndvitype, ndvidate, raintype, raindate ){
    if(raintype == "day"){
	selected_raindate = raindate;
    }else if(raintype == "dekad"){
	if (/^(\d{4})(\d{2})(\d{2})$/.test(raindate)){
	    year = RegExp.$1;
	    month = RegExp.$2;
	    day = RegExp.$3;
	    d = parseInt(day,10);
	    if( d < 11 ){
		dek = "1";
	    }else if(d > 20){
		dek = "3";
	    }else{
		dek = "2";
	    }
	    selected_rain = 'MPE_' + year + month + '_DEK' + dek;
	}
    }
    
    if(ndvitype == "month"){
	if (/^(\d{4})(\d{2})(\d{2})$/.test(ndvidate)){
	    year = RegExp.$1;
	    month = RegExp.$2;
	    day = RegExp.$3;
	    selected_ndvi =  'NDVI_' + year + month;
	}
    }
    else if(ndvitype == "16day"){
	selected_ndvi = "none";
    }
    
    // Set currentmap by checking for null in ndvitype and raintype
    NdviAndRainSelect( ndvitype, raintype );
    
    if(map){ map.setMapType(currentmap); }
    
    return;
}


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


function SelectMapType() {
}


function setupNDVI()
{
    
    SelectMapType.prototype = new GControl();
    
    SelectMapType.prototype.initialize = function(map) {
	var container = document.createElement("div");
	var selectNdviDiv = document.createElement("div");
	this.setButtonStyle_(selectNdviDiv);
	container.appendChild(selectNdviDiv);
	selectNdviDiv.appendChild(document.createTextNode("NDVI"));
	GEvent.addDomListener( selectNdviDiv, "click", function() {
				   map.setMapType(ndvimap);
				   currentmap = ndvimap;
			       });
	
	var selectRainDiv = document.createElement("div");
	this.setButtonStyle_(selectRainDiv);
	container.appendChild(selectRainDiv);
	selectRainDiv.appendChild(document.createTextNode("Rainfall"));
	GEvent.addDomListener( selectRainDiv, "click", function() {
				   map.setMapType(rainmap);
				   currentmap = rainmap;
			       });
	
	var selectBothDiv = document.createElement("div");
	this.setButtonStyle_(selectBothDiv);
	container.appendChild(selectBothDiv);
	selectBothDiv.appendChild(document.createTextNode("NDVI+Rain"));
	GEvent.addDomListener( selectBothDiv, "click", function() {
				   map.setMapType(bothmap);
				   currentmap = bothmap;
			       });
	
	map.getContainer().appendChild(container);
	return container;
    }

    SelectMapType.prototype.getDefaultPosition = function() {
	return new GControlPosition(G_ANCHOR_TOP_RIGHT, new GSize(7, 7));
    }
    
    SelectMapType.prototype.setButtonStyle_ = function(button) {
	button.style.textDecoration = "none";
	button.style.color = "#000000";
	button.style.backgroundColor = "white";
	button.style.font = "small Arial";
	button.style.fontSize = "12px";
	button.style.border = "1px solid black";
	button.style.padding = "2px";
	button.style.marginBottom = "3px";
	button.style.textAlign = "left";
	button.style.width = "6em";
	button.style.cursor = "pointer";
    }
    
    
    map = new GMap2(document.getElementById("map"));
    map.addControl(new GLargeMapControl());
    map.addControl(new GScaleControl());
    
    map.addControl(new SelectMapType());
    
    // Provide our own getTileUrl functions 
    
    CustomGetNdviTileUrl=function(a,b){
	return "http://www.wepoco.com/cgi/zoom2.py?type=ndvi&map="+selected_ndvi+"&x="+a.x+"&y="+a.y+"&zoom="+b
    }
    
    CustomGetRain1TileUrl=function(a,b){
	if(b>5){
	  return "/fetchzoom?type=mpe&map=MPE_"+
	    selected_raindate+"_M9_00"+"&x="+a.x+"&y="+a.y+"&zoom="+b
        }else{
	  return tilesite+"MPE_"+
	    selected_raindate+"_M9_00/"+b+"/"+a.x+"_"+a.y+".png"
	}
    }
    CustomGetRain2TileUrl=function(a,b){
        /*
        if(b>5){
	  return "http://localhost:8080/fetchzoom?type=mpe&map=MPE_"+
	selected_raindate+"_M7_57"+"&x="+a.x+"&y="+a.y+"&zoom="+b
        }else{
 	  return "http://wepoco.s3.amazonaws.com/mpe/MPE_"+
	    selected_raindate+"_M7_57/"+b+"/"+a.x+"_"+a.y+".png"
	}
	*/
	return "";
    }  

    
    var rainlayer1 = new GTileLayer(new GCopyrightCollection("Meteorological data: Wepoco"),2,5);
    var rainlayer2 = new GTileLayer(new GCopyrightCollection("Meteorological data: Wepoco"),2,5);
    
    var ndvilayer = new GTileLayer(new GCopyrightCollection("Meteorological data: Wepoco"),2,5);
    
    var rainlayers = [
		      G_HYBRID_MAP.getTileLayers()[0],
		      rainlayer1,rainlayer2,
		      G_HYBRID_MAP.getTileLayers()[1]
		      ];
    
    var ndvilayers = [
		      //G_NORMAL_MAP.getTileLayers()[0],
		      ndvilayer,
		      G_HYBRID_MAP.getTileLayers()[1]
		      ];
    
    var tilelayers = [
		      // G_NORMAL_MAP.getTileLayers()[0],
		      ndvilayer,
		      rainlayer1,rainlayer2,
		      G_HYBRID_MAP.getTileLayers()[1]
		      ];
    
    
    //tilelayers[0].getOpacity = function() {return 0.6;}
    
    //var ndvi_idx = 0;
    //var rain_idx = 1;
    
    rainlayer1.getTileUrl = CustomGetRain1TileUrl;
    rainlayer2.getTileUrl = CustomGetRain2TileUrl;
    rainlayer1.isPng = function() {return 1;}
    rainlayer2.isPng = rainlayer1.isPng;
    rainlayer1.getOpacity = function() {return 0.9;}
    rainlayer2.getOpacity = rainlayer1.getOpacity;
    rainlayer1.getCopyright = function(a,b) {
	return { prefix: "Meteorological Data:", copyrightTexts:["Wepoco"]};
    }
    rainlayer2.getCopyright = rainlayer1.getCopyright;

    
    ndvilayer.getTileUrl = CustomGetNdviTileUrl;
    ndvilayer.isPng = function() {return 1;}
    ndvilayer.getCopyright = function(a,b) {
	return { prefix: "Meteorological Data:", copyrightTexts:["Wepoco"]};
    }
    
    var maxres = 10;
    // == Create the GMapType, copying most things from G_SATELLITE_MAP ==
    var bothmap = new GMapType(tilelayers, G_SATELLITE_MAP.getProjection(), "Sat weather",
			       {maxResolution:maxres,minResolution:2,errorMessage:"error"});    
    
    var rainmap = new GMapType(rainlayers, G_SATELLITE_MAP.getProjection(), "Sat weather",
			       {maxResolution:maxres,minResolution:2,errorMessage:"error"});
    
    var ndvimap = new GMapType(ndvilayers, G_SATELLITE_MAP.getProjection(), "Sat weather",
			       {maxResolution:maxres,minResolution:2,errorMessage:"error"});
    
    // == Add the maptype to the map ==
    map.addMapType(bothmap);
    map.enableContinuousZoom();
    currentmap = rainmap;
    centre = getSavedLocation();
    if(centre == null){
	mapll = new GLatLng(10.0, 16.0);
        zoom = 3;
    }else{
	mapll = new GLatLng( centre[0], centre[1] );
        zoom = centre[2];
    }

    /* fix for high zoom in forecast view resulting in missing
     * data tiles in obs view.
     */
    if(zoom > 5){zoom = 5;}
    map.setCenter( mapll, zoom, currentmap);
    return;
}

