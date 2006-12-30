<?php 
  //header('Content-type: text/xml');
header('Content-type: application/vnd.google-earth.kml+xml');
header('Content-Disposition: attachment;filename=wepoco-ethiopia.kml');
//header('Cache-Control: no-cache, must-revalidate');
//header('Last-Modified: Sat, 1 Jan 2000 00:00:00 GMT');

$urlbase = "http://home.badc.rl.ac.uk/astephens/ncep_data/";


function url($id)
{
  global $urlbase;
  $now = time();
  $yesterday = $now - 24*60*60;
  $hour = gmdate("H", $now);
  if($hour < 10){
    $date = gmdate("Ymd", $yesterday) . "00";
  }else{
    $date = gmdate("Ymd", $now) . "00";
  }
  return $urlbase . "${date}_${id}_rainfall.gif";
}

function desc($id)
{
  $imgsrc = url($id);
  $text = <<<HERE
<description><![CDATA[
 <div style="width:360px;height:295px" class="info-window">
 <img style="margin-top:-45px;margin-left:-20px;position:absolute;clip:rect(45px 380px 340px 20px)" 
 src="${imgsrc}"  />
 </div>
]]></description>
HERE;
  echo $text;
}

?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Folder>
<name>Ethiopia</name>
  <Placemark>
  <!-- <marker label="Addis Ababa" id="addis_ababa" lat="9.015" lng="38.738" level="3" /> -->
  <name>Addis Ababa</name>
  <?php desc('addis_ababa') ?>
  <Point>
    <coordinates>38.738,9.015,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Mekele" id="mekele" lat="13.507" lng="39.474" level="4" /> -->
  <name>Mekele</name>
  <?php desc('mekele') ?>
  <Point>
    <coordinates>39.474,13.507,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Gonder" id="gonder" lat="12.619" lng="37.474" level="5" /> -->
  <name>Gonder</name>
  <?php desc('gonder') ?>
  <Point>
    <coordinates>37.474,12.619,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Bahir Dar" id="bahir_dar" lat="11.588" lng="37.375" level="5" /> -->
  <name>Bahir Dar</name>
  <?php desc('bahir_dar') ?> 
  <Point>
    <coordinates>37.375,11.588,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Dese" id="dese" lat="11.08" lng="39.67" level="5" /> -->
  <name>Dese</name>
<?php desc('dese') ?>
  <Point>
    <coordinates>39.67,11.08,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Debre Markos" id="debre_markos" lat="10.33" lng="37.67" level="5" /> -->
  <name>Debre Markos</name>
<?php desc('debre_markos') ?>
  <Point>
    <coordinates>37.67,10.33,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Nekemte" id="nekemte" lat="9.07" lng="36.5" level="4" /> -->
  <name>Nekemte</name>
<?php desc('nekemte') ?>
  <Point>
    <coordinates>36.5,9.07,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Dembi Dolo" id="dembi_dolo" lat="8.527" lng="34.805" level="5" /> -->
  <name>Dembi Dolo</name>
  <Point>
    <coordinates>34.805,8.527,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Jima" id="jima" lat="7.67" lng="36.78" level="5" /> -->
  <name>Jima</name>
<?php desc('jima') ?>
  <Point>
    <coordinates>36.78,7.67,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Nazret" id="nazret" lat="8.53" lng="39.37" level="5" /> -->
  <name>Nazret</name>
<?php desc('nazret') ?>
  <Point>
    <coordinates>39.37,8.53,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Jijiga" id="jijiga" lat="9.33" lng="42.83" level="5" /> -->
  <name>Jijiga</name>
<?php desc('jijiga') ?>
  <Point>
    <coordinates>42.83,9.33,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Arba Minch" id="arba_minch" lat="6.00" lng="37.50" level="4" /> -->
  <name>Arba Minch</name>
<?php desc('arba_minch') ?>
  <Point>
    <coordinates>37.5,6.00,0</coordinates>
  </Point>
  </Placemark>
  <Placemark>
  <!-- <marker label="Dire Dawe" id="dire_dawe" lat="9.590" lng="41.869" level="4" /> -->
  <name>Dire Dawe</name>
<?php desc('dire_dawe') ?>
  <Point>
    <coordinates>41.869,9.590,0</coordinates>
  </Point>
  </Placemark>
</Folder>
</kml>
