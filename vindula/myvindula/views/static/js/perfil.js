$j = jQuery.noConflict();

function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}

$j(document).ready(function(){
	var session = getURLParameter('session');
    
	if(session){
		$j('#'+session).addClass('active');
	};
    
    $j('.section-user-profile .icon-moreaccess a.more').click(function(ev){
        var section = this.id || false;
        
        if(section){
            $(this).parents('section.active').removeClass('active');
            $('section#'+section).addClass('active');
        }
        
        return false;
    })
    
});