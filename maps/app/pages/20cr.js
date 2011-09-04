// 20cr.js
// Michael Saunby. Aug 2011
//
// N.B. depends on Dojo

// call as coords20cr({latlng:latlng,load:function(d){STUFF},error:function(msg){STUFF})
function coords20cr(vals) {
/*
   dojo.xhrGet({
        url:"/cgi-bin/py/coords20cr.py", 
	content:{lat:vals.latlng.lat(),lng:vals.latlng.lng()},
	handleAs:"json",
        load: vals.load,
        error: vals.error});
*/
   dojo.io.script.get({
        //Cross domain works - use this URL
        url: "http://saunby.net/cgi-bin/py/coords20cr.py",
	content:{lat:vals.latlng.lat(),lng:vals.latlng.lng()},
        callbackParamName: "callback",
        load: vals.load,
        error: vals.error});
}

// call as series20cr({cell:{x:x,y:y},load:function(d){STUFF},error:function(msg){STUFF})
function series20cr(vals) {
/*
   dojo.xhrGet({
        url:"/cgi-bin/py/series20cr.py", 
	content:{x:vals.cell.x,y:vals.cell.y,q:vals.quantity},
	handleAs:"json",
        load: vals.load,
        error: vals.error});
*/
   dojo.io.script.get({
        url:"http://saunby.net/cgi-bin/py/series20cr.py", 
       content:{x:vals.cell.x,y:vals.cell.y,q:vals.quantity},
        callbackParamName: "callback",
	handleAs:"json",
        load: vals.load,
        error: vals.error});
}



