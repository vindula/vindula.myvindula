/* FONTE: popupforms.js - */
$j = jQuery.noConflict();

function mostraFoto(e,m){
    var user = $j('#username').val();
    var html = '';
    var rand = Math.floor(Math.random()*100)
    var campo = m.find('#field').val()
    
    html +='<img height="150px" src="/user-image?username='+user+'&field='+campo+'&x='+rand+'"/><br /> ';

    if (user != 'undefined') {
        $j('div#preview-user-'+campo).html(html);
        $j('a.excluir-foto').show();
     }
 };

function RemoveFoto(e,m){
    var campo = m.find('#field').val()
     $j('div#'+campo +' div#preview-user-'+campo).html('');
     $j('div#'+campo +' a.excluir-foto').hide();
 };

$j(document).ready(function(){
	
    var common_content_filter = '#content=*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';
    var common_jqt_config = {fixed:false,speed:'fast',mask:{color:'#000',opacity: 0.4,loadSpeed:0,closeSpeed:0}};

   // Visual dialog
   $j('a.crop-foto').prepOverlay({
        subtype: 'ajax',
        filter: common_content_filter,
        formselector: 'form[name=crop_image]',
        noform: 'close',
        width: '50%',
        afterpost: function (resp, elem) { 
			CarregaCrop(resp, elem);
		},
		beforepost: function (resp, elem) {
			if (resp.find('input[type="submit"]').val() == "Cortar")
			{
				if ((resp.find('#cort-x').val() && resp.find('#cort-y').val() && resp.find('#cort-x2').val() && resp.find('#cort-y2').val()) &&
				    (resp.find('#cort-x').val() != resp.find('#cort-x2').val() && resp.find('#cort-y').val() != resp.find('#cort-y2').val()))
				{
					return true;
				}
				alert("Por favor, selecione a area que deseja cortar antes de salvar.")
				return false;				
			}
			
			return true;
		},
        config: {
			fixed:false,
			speed:'fast',
			mask:{color:'#000', opacity: 0.4, loadSpeed:0, closeSpeed:0},
            onBeforeClose:function (e) {
				mostraFoto(e,this.getOverlay()); 
			}
		}
   });
   common_jqt_config['onBeforeClose'] = function (e) {RemoveFoto(e,this.getOverlay());};
   $j('a.excluir-foto').prepOverlay({
        subtype: 'ajax',
        formselector: 'form[name=exclud-user]',
        noform: 'close',
        filter: common_content_filter,
        config: common_jqt_config,
        width:'20%'
        
   });
    
});