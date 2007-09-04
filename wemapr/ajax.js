
function makeHttpRequest(url, callback_function, return_xml)
{
    var http_request = false;

    if (window.XMLHttpRequest) { // Mozilla, Safari,...
        http_request = new XMLHttpRequest();
        if (http_request.overrideMimeType) {
            http_request.overrideMimeType('text/xml');
        }
    } else if (window.ActiveXObject) { // IE
        try {
            http_request = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try {
                http_request = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e) {}
        }
    }

    if (!http_request) {
        alert('Unfortunatelly you browser doesn\'t support this feature.');
        return false;
    }
    http_request.onreadystatechange = function() {
        if (http_request.readyState == 4) {
            if (http_request.status == 200) {
                if (return_xml) {
                    eval(callback_function + '(http_request.responseXML)');
                } else {
                    eval(callback_function + '(http_request.responseText)');
                }
            } else {
                // alert('There was a problem with the request.(Code: ' + http_request.status + ')');
            }
        }
    }
    http_request.open('GET', url, true);
    http_request.setRequestHeader( "If-Modified-Since", "Sat, 1 Jan 2000 00:00:00 GMT" );
    http_request.send(null);
}

function _paramObj( name, value ){
  this.name = name;
  this.value = encodeURI( value );
  this.getValue = function(){ return decodeURI(this.value); }
}

function ParamArray(){
 this.store = new Array();
 this.pushNameValue = function( name, value ){ 
    this.store.push(new _paramObj(name, value)); 
 } 
 this.popURI = function(){ 
    var text = "";
    p=this.store.pop()
    if(p){
      text += "?" + p.name +"="+ p.value;
    }
    while( p=this.store.pop() ){
      text += "&" + p.name +"="+ p.value;
    }
    return text;
 }
 return this;
}

function decodeSearch(location){
  loc = location.search.substring(1);
  return loc.split('&');
}