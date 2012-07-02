$j = jQuery.noConflict();

function confirmExcluir(){
		if (confirm('Tem certeja que deseja excluir este usuário?')){
			return true;
		}else{
			return false;
		}
	};

function confirmAlterarUserName () {
    var username = $j('#username').val();
    var username_old = $j('#username-old').val();
    
    if (username != username_old){
        if (confirm('Todas as informações criadas pelo antigo username serão excluídas. Deseja confirmar alteração?')){
            return true;
        }else{
            return false;
        }         
    }else{
        return true;      
    }
}

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