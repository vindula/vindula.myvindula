$j = jQuery.noConflict();

function  createElement(name) {
    return $(document.createElement(name));
}

function defineLinkModal() {
    
    $j('a.profile-link, a.structure-link').live({
        mouseenter: function (ev) {
            clearTimeout($j(this).data('timeout_out'));
            var $el = $j(this),
                JQ_height = $el.height() || 0,
                JS_height = this.height || 0;
            
            
            var height = Math.max(JQ_height, JS_height);
            
            var t_in = setTimeout(function() {
                if($el.find('.vindula-modal').length){
                    $el.find('.vindula-modal').show();
                }else{
                    var content_value = $el.attr('data-value'),
                        base_url = $j('base').attr('href'),
                        type_of_modal = $el.attr('data-type');
                    
                    if (type_of_modal == 'UserObject'){
                        modal_url = base_url+'/modal-profile';
                    }else{
                        modal_url = base_url+'/modal-structure';
                    }
        
                    $j.ajax({
                        type: "POST",
                        url: modal_url,
                        data: {content_value: content_value},
                        success: function(data){
                            $dom = $j(data);
                            $dom.css('top', height+10);
                            $dom.find('.social-info').vindula(null, {user_token: window.token});
                            $el.append($dom);
                        }
    //                    error: function(error){
    //                        console.error(error);
    //                    }
                    })
                }
            }, 1000);
        
            $j(this).data('timeout_in', t_in);
        },
        mouseleave: function (ev) {
            clearTimeout($j(this).data('timeout_in'));
        
            var $el = $j(this);
            var t_out = setTimeout(function() {
                if ($el.find('.vindula-modal').length) {
                    $el.find('.vindula-modal').hide();
                }
            }, 500);
            
            $j(this).data('timeout_out', t_out);
        }
    });
    
//    $j('a.profile-link, a.structure-link').hover(function (ev) {
//        clearTimeout($j(this).data('timeout_out'));
//        var $el = $j(this),
//            JQ_height = $el.height() || 0,
//            JS_height = this.height || 0;
//        
//        
//        var height = Math.max(JQ_height, JS_height);
//        
//        var t_in = setTimeout(function() {
//            if($el.find('.vindula-modal').length){
//                $el.find('.vindula-modal').show();
//            }else{
//                var content_value = $el.attr('data-value'),
//                    base_url = $j('base').attr('href'),
//                    type_of_modal = $el.attr('data-type');
//                
//                if (type_of_modal == 'UserObject'){
//                    modal_url = base_url+'/modal-profile';
//                }else{
//                    modal_url = base_url+'/modal-structure';
//                }
//    
//                $j.ajax({
//                    type: "POST",
//                    url: modal_url,
//                    data: {content_value: content_value},
//                    success: function(data){
//                        $dom = $j(data);
//                        $dom.css('top', height+10);
//                        $dom.find('.social-info').vindula(null, {user_token: window.token});
//                        $el.append($dom);
//                    }
////                    error: function(error){
////                        console.error(error);
////                    }
//                })
//            }
//        }, 1000);
//        
//        $j(this).data('timeout_in', t_in);
//    },function (ev) {
//        clearTimeout($j(this).data('timeout_in'));
//        
//        var $el = $j(this);
//        var t_out = setTimeout(function() {
//            if ($el.find('.vindula-modal').length) {
//                $el.find('.vindula-modal').hide();
//            }
//        }, 500);
//        
//        $j(this).data('timeout_out', t_out);
//    });
    
}

$j(document).ready(function(){
    defineLinkModal();
});