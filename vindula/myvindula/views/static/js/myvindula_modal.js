$j = jQuery.noConflict();

function  createElement(name) {
    return $(document.createElement(name));
}

$j(document).ready(function(){
    
    $('a.profile-link').hover(function (ev) {
        var $el = $j(this),
            JQ_height = $el.height() || 0,
            JS_height = this.height || 0;
        
        
        var height = Math.max(JQ_height, JS_height);
        
        var t = setTimeout(function() {
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
        
        $(this).data('timeout', t);
    },function (ev) {
        clearTimeout($(this).data('timeout'));
        var $el = $j(this);
        
        if ($el.find('.profile-modal').length) {
            $el.find('.profile-modal').hide();
        }
    });
    
 });