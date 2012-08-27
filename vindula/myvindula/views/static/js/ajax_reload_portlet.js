$j = jQuery.noConflict();

$j(document).ready(function(){
	
	function reloadPortlet(){

		var url = $j('#url').val() + '/reload-aniversariantes'
		var quantidade = $j('#quantidade').val();
		var tipo_busca = $j('#tipo_busca').val();
		var show_picture = $j('#show_picture').val();
		var details_user = $j('#details_user').val();
		var search_random = $j('#search_random').val();
		var principal_user = $j('#principal_user').val();
				
		var max_result = $j('#max_result').val();
		
		if (parseInt(max_result) > parseInt(quantidade)) {
			$j('#b_start').val(sequencia(quantidade,$j('#b_start').val(), max_result));
		};

		var b_start = $j('#b_start').val();

		$j.get(url,{quantidade:quantidade,
 				    type_search:tipo_busca,
					show_picture:show_picture,
					details_user:details_user,
					search_random:search_random,
					principal_user:principal_user,
					b_start:b_start}, function(data){
			
				if (div == 1) {
					$j('#reload-data-protlet-A').html(data);
					$j('#reload-data-protlet-B').html('');
					
					heightDiv($j('#reload-data-protlet-A'));
					div = 2;
					
				}else{
					$j('#reload-data-protlet-B').html(data);
					$j('#reload-data-protlet-A').html('');
					
					heightDiv($j('#reload-data-protlet-B'));
					div = 1;
				}
		});
		$j('#next-page').trigger('click');
	};
	
	function sequencia(quant, b_start, max_result){
		if (max_result != null){
			var x = parseInt(b_start) + parseInt(quant)
			if(parseInt(x) < parseInt(max_result)){return x;
			}else{return 0}
			
		}else{return 0;}
	};
	
	function heightDiv(div){
		var altura = div.height();
		$j('.aniversante-cycle').css('height',altura+'px');
	};

	/*
	$j('body').click(function(){
		reloadPortlet();	
	});*/
	
	var div = 1 
	reloadPortlet();
	
	var tempo_rotacao = $j('#tempo_rotacao').val();
	window.setInterval(function(){
		reloadPortlet();
	},parseInt(tempo_rotacao));
	
	$j('.aniversante-cycle').cycle({
	    fx:     'scrollHorz',
	    speed:   1000,
	    timeout: 0,
		next: 	'#next-page',
		delay: 800
		});
    
});