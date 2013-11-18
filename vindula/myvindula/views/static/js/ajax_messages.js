$j = jQuery.noConflict();

$j(document).ready(function(){
    $j('.delete-message').live('click', function(){
        
        if (confirm('Realmente deseja remover a mensagem?')) {
            var $super_this = $j(this),
                hash = $super_this.attr('data-hash'),
                url = this.href + '/' + window.token + '/';
                
            if(hash.length) {
                $j.ajax({   
                    type: "GET",
                    url: url,
                    data: {'hash': hash},
                    success: function(data){
                        if(data.status){
                            $item_ele = $super_this.parents('.item_lista');
                            $item_ele.hide();
                        }else{
                            alert('Não foi possível remover a mensagem.');
                        }
                    }
                });
            }else {
                alert('Não foi possível remover a mensagem.');
            }
        }
        
        return false;
    });
});
