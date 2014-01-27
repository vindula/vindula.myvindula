$j = jQuery.noConflict();

function executaAjax(ctx, b_start, b_size){
    var url = $j('base').attr('href') + 'myvindulalistrecados',
        usernames = ctx.find('.usernames').val(),
        data_inicial = ctx.find('#datepicker_data_inicial').val(),
        data_final = ctx.find('#datepicker_data_final').val();
        params = {};


    if (b_start==null) {
        b_start = parseInt(ctx.find('input#b_start').val());
        if (isNaN(b_start)) {
            b_start = parseInt(ctx.children().find('input#b_start').val());
        }
    }
        
    if (b_size==null) {
        b_size = parseInt(ctx.find('input#b_size').val());
        if (isNaN(b_size)) {
            b_size = parseInt(ctx.children().find('input#b_size').val());
        }
    }
    
    params['b_size'] = b_size;
    params['b_start'] = b_start;
    params['ajax_load'] = 1;
    
    if (usernames){
        params['usernames'] = usernames;
    }
    
    if (data_inicial){
        params['data_inicial'] = data_inicial;
    }
    
    if (data_final){
        params['data_final'] = data_final;
    }


    ctx.find('.ajax_loader').show();
    ctx.find('div.content-pagination').css('opacity', '0.2');
    ctx.find('.submet_seach').css('opacity', '0.2');

    $j.ajax({
        url: url,
        data: params,
        type: 'POST',
        success: function(data){

            var result = $j(data).find('#content_recados');
            $j('#content_recados').html(result.contents());
            
            if ($j('#content_recados').find('.social-box').length){
                $j('#content_recados').find('.social-box').vindula(null, {user_token: window.token});    
            }

            ctx.find('.ajax_loader').hide();
            ctx.find('div.content-pagination').css('opacity', '1');
            ctx.find('.submet_seach').css('opacity', '1');
        }
    });
}



$j(document).ready(function(){

    $j(".usernames").tokenInput(autoCompleteUser,{queryParam: 'term',        
                                                theme: "facebook",
                                                i18n:'pt_BR'});

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

    $j('.submet_seach').click(function(){
        var $conteiner = $j(this).parents('.userpage');

        executaAjax($conteiner,null,null);

    });


    $j('div#cycle-next, div#cycle-prev').live('click',function(){
        var $conteiner = $j(this).parents('.userpage'),
            b_start = parseInt($j(this).find('input').val());

        executaAjax($conteiner,b_start,null);
    });
    

    $j('div#size-nav a').live('click',function(event){
        event.preventDefault();
        event.stopPropagation();
        var $conteiner = $j(this).parents('.userpage'),
            b_size = parseInt($j(this).text());

        executaAjax($conteiner,null,b_size);
    });

    $j.datepicker.setDefaults($j.datepicker.regional["pt-BR"]);
    var D = {showAnim:'blind',
             dateFormat: "dd/mm/yy",
             defaultDate: "1D",
             numberOfMonths: 1,
             minDate: "-5Y"
            };
    
    $j('#datepicker_data_inicial').datepicker(D);
    $j('#datepicker_data_final').datepicker(D);

});
