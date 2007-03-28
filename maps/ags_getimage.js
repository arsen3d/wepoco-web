<html>
   <head>
<title>Javascript for image getting</title>

<script type="text/javascript" language="javascript"> 

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
    var urlbase="http://home.badc.rl.ac.uk/astephens/ncep_data/";
    var today=new Date();
    var hour=today.getHours();
    if (hour<10) { // use yesterday
        today=getLatestDate(-1);
    } else {
        today=getLatestDate(0);
    }
    var datetime=today+"00";
    var url=urlbase+datetime+"_"+location+"_rainfall.gif";
    //alert(url);
    return url;
}


function getPicture(location) {
    // fix src of picture like in my example
    var img=document.getElementById("timeseriesplot");
    var loc=location.toLowerCase().replace(" ","_");
    img.src=getLatestURL(loc);

}

function showMarkers( map ) {

  GDownloadUrl("markers.xml", function(data, responseCode) {
    var xml = GXml.parse(data);
    var markers = xml.documentElement.getElementsByTagName("marker");
    for (var i = 0; i < markers.length; i++) {
      var point = new GLatLng(parseFloat(markers[i].getAttribute("lat")),
                            parseFloat(markers[i].getAttribute("lng")));
      var text = markers[i].getAttribute("label");
      map.addOverlay( createMarker(point, text) );
    }
  });
}

</script>
</head>
<body>
<P>Click these to get the latest file for "Dembi Dolo" or "Addis Abeba":</P>
<A NAME="hi" ONCLICK="getPicture('Dembi Dolo')">Dembi Dolo</A>
<A NAME="hi" ONCLICK="getPicture('Addis Ababa')">Addis Ababa</A>
<P><IMG SRC="" ID="timeseriesplot"/></P>
</body>
</html>

