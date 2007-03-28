// forecasts.js
// Michael Saunby.  For Wepoco.
//

var map = null;

function SetupMap() {
  map = new GMap2(document.getElementById("map"));
  map.addControl(new GLargeMapControl());
  map.addControl(new GScaleControl());

  centre = getSavedLocation();
  if(centre == null){
    mapll = new GLatLng(10.0, 16.0);
    zoom = 3;
  }else{
     mapll = new GLatLng( centre[0], centre[1] );
     zoom = centre[2];
  }
  map.setCenter( mapll, zoom );
  window.setTimeout( setupMarkers, 0);
  return;
}

function setupMarkers() {
   showMarkers( map );
   return;
}
