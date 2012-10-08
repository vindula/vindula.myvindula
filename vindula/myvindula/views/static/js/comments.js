$j = jQuery.noConflict();

function confirmExcluir(){
		if (confirm('Tem certeja que deseja excluir este usuário?')){
			return true;
		}else{
			return false;
		}
	};

$j(document).ready(function(){	
	$j('#cancel-coment').live('click',function(){
		$j(this).parent().parent().parent().parent().find('#new-comments').css('display','none');
		$j(this).parent().parent().parent().parent().find('.bt_comments').eq(0).css('display', '')
	   
	});
	$j('input[name="url_context"]').attr('value',location);
	
	$j('div.geral_lista_comentarios span#number-comments').click(function() {
		var comments = $j(this).parent().parent().find('.comments-cont');
		var text = $j(this).parent().find('span#show-hide');
		
		if (comments.css('display') == 'none') {
			comments.show();
			text.text(' Ocultar');
		}
		else {
			comments.hide();
			text.text(' Ver');
		}
	})
	
});	