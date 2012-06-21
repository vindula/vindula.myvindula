$j = jQuery.noConflict();

$j(document).ready(function(){

	$j('#howareu').hide();
	$j('#scraps').hide();
	$j('#perfil').show();
			
	var variaveis = location.search.split("?");
	var scraps = variaveis[1].lastIndexOf("scraps");
	if (scraps != -1){
		$j('#howareu').hide();
		$j('#scraps').show();
		$j('#perfil').hide();
		
		$j('#howareu-menu').removeClass('selected');
		$j('#scraps-menu').addClass('selected');
		$j('#perfil-menu').removeClass('selected');
		
	};	  
	
	$j('#howareu-menu').click(function(){
		$j('#howareu').show();
		$j('#scraps').hide();
		$j('#perfil').hide();
			
		
		$j('#howareu-menu').addClass('selected');
		$j('#scraps-menu').removeClass('selected');
		$j('#perfil-menu').removeClass('selected');
	});
	
	
	$j('#scraps-menu').click(function(){
		$j('#howareu').hide();
		$j('#scraps').show();
		$j('#perfil').hide();
		
		$j('#howareu-menu').removeClass('selected');
		$j('#scraps-menu').addClass('selected');
		$j('#perfil-menu').removeClass('selected');
	});
	
	
	$j('#perfil-menu').click(function(){
		$j('#howareu').hide();
		$j('#scraps').hide();
		$j('#perfil').show();
		
		$j('#howareu-menu').removeClass('selected');
		$j('#scraps-menu').removeClass('selected');
		$j('#perfil-menu').addClass('selected');
	});
	
});