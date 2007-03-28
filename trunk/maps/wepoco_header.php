<script type="text/javascript" language="javascript">
   function minimize(){
    hdr=document.getElementById("header");
    hdr.style.height = "2px";
    hdr.style.visibility = "hidden";
   }
   function maximize(){
    hdr=document.getElementById("header");
    hdr.style.height = "130px";
    hdr.style.visibility = "visible";
   }
</script>
<div style="position:absolute; right:0; top:0; z-index:3; cursor:pointer">
  <a style="background-color:white;color:black;border:1px solid black;
     padding:2px; font:small Arial; marginBottom:3px" onclick="minimize()">min</a>
  <a style="background-color:white;color:black;border:1px solid black;
     padding:2px; font:small Arial; marginBottom:3px" onclick="maximize()">max</a> 
</div>
<div id="header" style=
     "background:#FFFFff;width:660px;height:130px;margin-top:0;border:0;padding:0;left:0;position:relative;">
     <div id="wepoco">
       <img alt="wepoco: making weather and climate information useful "
       src="/wepoco-look/logo_small_text30_circ.gif" style="width:531px; height:130px;" />
     </div>
     <div id="wepoco-nav-right" style="z-index:2" >
       <ul>
         <li><a href="/?page_id=14">About us</a></li>
         <li><a href="/?page_id=14">Can we help you?</a></li>
         <li><a href="/?page_id=14">Can you help us?</a></li>
         <li><a href="/?page_id=13">Developers' corner</a></li>
       </ul>
     </div><!-- wepoco-nav-right -->
</div><!-- header -->
     <div id="wepoco-nav" style="position:relative;z-index:3" >
       <ul style="width:100%">
       <li><a href="/">home</a></li>
       <?php
         if ($wepoco_selected == 'observations') {
           echo '<li><a class="selected" >observations</a></li>';
         } else {
           echo '<li><a href="observations.php" >observations</a></li>';
         }
         if ($wepoco_selected == 'forecasts') {
           echo '<li><a class="selected" >forecasts</a></li>';
         } else {
           echo '<li><a href="forecasts.php" >forecasts</a></li>';
         }
       ?>
       <li><a href="/">comment & news</a></li>
       <li><a href="/?page_id=15">links</a></li>
       </ul>
     </div><!-- wepoco-nav -->

