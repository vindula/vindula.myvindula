$j = jQuery.noConflict();

function doCycle(el, next){
    
    if(!el.hasClass('disabled')){
        var $container_cycle = el.parent(),
            $selected = $container_cycle.find('li.active'),
            $change = false,
            $parent_change = false;
        
        if(next) {
            $change = $selected.next('li');
            var $el_parent = el.prev('a');
            if ($change.length) {
                $parent_change = $change.next('li');
            }
        }else {
            $change = $selected.prev('li');
            var $el_parent = el.next('a');
            if ($change.length) {
                $parent_change = $change.prev('li');
            }
        }
        
        if (!$change.length){
            return false;
        }
        
        if ($change){
            $change.addClass('active');
            $selected.removeClass('active');
            $change.toggle();
            $selected.toggle();
            $el_parent.removeClass('disabled');
            if(!$parent_change.length){
                el.addClass('disabled');
            }
        }
        
        return $change;
    }
    
    return false;
}


$j(document).ready(function(){
    
    $j('a.cycle-prev').live('click', function(ev){
       var $this = $j(this);
       doCycle($this, false);
       
       return false;
    });
    
    $j('a.cycle-next').live('click', function(ev){
       var $this = $j(this);
       doCycle($this, true);
       
       return false;
    });
    
});
