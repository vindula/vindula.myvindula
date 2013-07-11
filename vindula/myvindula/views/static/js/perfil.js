$j = jQuery.noConflict();

function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}

$j(document).ready(function(){
	var session = getURLParameter('session');
    
	if(session){
		$j('#'+session).addClass('active');
	};
    
});