// 20cr.js
// Michael Saunby. Aug 2011
//
// N.B. depends on Dojo

// call as coords20cr({latlng:latlng,load:function(d){STUFF},error:alert})
function coords20cr(vals) {
   dojo.xhrGet({
        url:"/py/coords20cr.py", 
	       content:{lat:vals.latlng.lat(),lng:vals.latlng.lng()},
	handleAs:"json",
        load: vals.load,
        error: vals.error});
   return 0;
}

