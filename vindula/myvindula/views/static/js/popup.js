/* FONTE: popupforms.js - */
$j = jQuery.noConflict();

function mostraFoto(){
    var user = $j('#username').val();
    var html = '';
    var rand = Math.floor(Math.random()*100)
    
    html +='<img height="150px" src="/user-image?username='+user+'&x='+rand+'"/><br /> ';

    if (user != 'undefined') {
        $j('div#preview-user').html(html);
        $j('a.excluir-foto').show();
        var end = document.getElementById('pb_1').getElementsByTagName('iframe')[0].src;
        document.getElementById('pb_1').getElementsByTagName('iframe')[0].src = '';
        document.getElementById('pb_1').getElementsByTagName('iframe')[0].src = end;
     }
 };

function RemoveFoto(){
     $j('div#preview-user').html('');
     $j('a.excluir-foto').hide();
 };

$j(document).ready(function(){
	
    var common_content_filter = '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';
    var common_jqt_config = {fixed:false,speed:'fast',mask:{color:'#000',opacity: 0.4,loadSpeed:0,closeSpeed:0}, height:'400px'};

    // Visual dialog
   
   $j('a.crop-foto').prepOverlay({
        subtype: 'iframe',
        config: common_jqt_config,
        width:'50%'
   });
   
   $j('a.excluir-foto').prepOverlay({
        subtype: 'iframe',
        config: common_jqt_config,
        width:'20%'
   });
   
   $j('a.excluir-foto').click(function(){
       var height = '150px';
       $j('div.overlay iframe').css('height', height);
       
   });
   
        
   $j('a.crop-foto').click(function(){
       var height = (window.innerHeight - 22 )*0.7 +'px';
       $j('div.overlay iframe').css('height', height);
       
   });
});