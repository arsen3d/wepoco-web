<?php

  // Michael Saunby for Wepoco.

$type= $_REQUEST['type'];
$map = $_REQUEST['map'];
$x =  $_REQUEST['x'];
$y =  $_REQUEST['y'];
$z =  $_REQUEST['zoom'];

$exten = ".png";
$contenttype = "image/png";

$datadir = "/home/wepoco/ftp/" . $type . "/" . $map . "/";
$NO_DATA = "/home/wepoco/ftp/mpe/" . "no_data" . $exten;

$filename = $datadir . $z . "/" . $x . "_"  . $y . $exten;

header( 'Content-type: ' . $contenttype );
@readfile( $filename ) or
		 readfile( $NO_DATA );
?>
