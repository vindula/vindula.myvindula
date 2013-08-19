$j = jQuery.noConflict();

function  createElement(name) {
    return $(document.createElement(name));
}

$j(document).ready(function(){
    
    $j('a.profile-link').hover(function (ev) {
        clearTimeout($j(this).data('timeout_out'));
        var $el = $j(this),
            JQ_height = $el.height() || 0,
            JS_height = this.height || 0;
        
        
        var height = Math.max(JQ_height, JS_height);
        
        var t_in = setTimeout(function() {
            if($el.find('.profile-modal').length){
                $el.find('.profile-modal').show();
            }else{
                var username = $el.attr('data-username'),
                    base_url = $j('base').attr('href'),
                    modal_url = base_url+'/modal-profile';
    
                $j.ajax({
                    type: "POST",
                    url: modal_url,
                    data: {username: username},
                    success: function(data){
                        $dom = $j(data);
                        $dom.css('top', height+10);
                        $dom.find('.social-info').vindula(null, {user_token: window.token});
                        $el.append($dom);
                    },
                    error: function(error){
                        console.error(error);
                    }
                })
            }
        }, 1000);
        
        $j(this).data('timeout_in', t_in);
    },function (ev) {
        clearTimeout($j(this).data('timeout_in'));
        
        var $el = $j(this);
        var t_out = setTimeout(function() {
            if ($el.find('.profile-modal').length) {
                $el.find('.profile-modal').hide();
            }
        }, 500);
        
        $j(this).data('timeout_out', t_out);
    });
    
 });