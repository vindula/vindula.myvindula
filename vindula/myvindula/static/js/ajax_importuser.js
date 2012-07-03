$j = jQuery.noConflict();

$j(document).ready(function(){

	function ajaxImport(cont,i){
		$j('div#spinner').removeClass('display-none');
		var url = $j('#portal_url').val() + "/ajax_view";
		
		$j.get(url,{numb_user:i, method:'importUser' }, function(data){
				$j('#users_import').html($j('#users_import').html()+data);
				$j('#spinner').addClass('display-none');
				i++;
				if (i<cont){
					ajaxImport(cont,i);
				};
			});
	};
	
	$j('input#voltar').click(function(){
		var url = $j('#portal_url').val() + "/@@overview-controlpanel";
		location.href=url;
	});
	
	$j('input#importUser').click(function(){
		
		

		if (confirm('Tem certeza que deseja importar os usuários?')){
			var cont = $j('#contUser').val()
			var i = 0;
			ajaxImport(cont,i);
		}
		else{
				return false;
				
		};
		
		
		
		
	
	});
});
