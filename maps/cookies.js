// cookies.js
// Michael Saunby.  For Wepoco.
//

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
function saveLocation( map /* GMap2 class */ ) {
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
