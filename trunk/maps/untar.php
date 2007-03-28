<?php
$archname = $_GET['tgz'];
?>
<h1><?php echo $archname; ?></h1>
<p>
<?php
chdir( '/home/wepoco/ftp/mpe' );
pclose( popen('tar zxf '.$archname, 'r') );
?>
</p>
