$j = jQuery.noConflict();

$j(document).ready(function(){

	$j('select#select-holerite').change(function(){
		if ($j(this).val()) {
			var url = $j('#portal_url').val() + "/myvindula-find-holerite";
			var id = $j(this).val();
			$j('#spinner').removeClass('display-none');
			$j('#holerite').addClass('display-none');
			
			$j.get(url, {
				id: id,
			}, function(data){
			
				$j('#holerite-cont').html(data);
				$j('#holerite-cont').removeClass('display-none');
				$j('#spinner').addClass('display-none');
			});
		}
	});
    
    $j('#cpf_validate').keypress(function(){
        Mascara(this,Cpf);
    });
});