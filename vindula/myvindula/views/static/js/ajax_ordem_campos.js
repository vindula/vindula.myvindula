$j = jQuery.noConflict();

// Return a helper with preserved width of cells
var fixHelper = function(e, ui) {
    ui.children().each(function() {
        $j(this).width($j(this).width());
    });
    return ui;
};


$j(document).ready(function(){
    $j(".sortable").sortable({
        helper: fixHelper,
        update: function(event, ui) {
                    var result = $j(this).sortable('toArray');
                    var url = 'http://' + window.location.hostname + "/ordem_myvindulaconfgs";
       
                    $j.get(url,{list:result.toString()}, function(data){
                            
                    });
                }
    }).disableSelection();
});
