$j = jQuery.noConflict();
                        
function exibePreview(c){
    var rx = 100 / c.w;
    var ry = 100 / c.h;
    var img = document.getElementById('usertImage'); 
    //or however you get a handle to the IMG
    var img_width = img.width;
    var img_height = img.height;
    
    // atualiza CSS do preview para refletir o tamanho da imagem enviada
    // e o posicionamento do crop
    $j('#preview').css({
        width: Math.round(rx * img_width) + 'px',
        height: Math.round(ry * img_height) + 'px',
        marginLeft: '-' + Math.round(rx * c.x) + 'px',
        marginTop: '-' + Math.round(ry * c.y) + 'px'
    });
    
    // campos hidden que armazenam os valores
    $j('#cort-x').val(c.x);
    $j('#cort-y').val(c.y);
    $j('#cort-x2').val(c.x2);
    $j('#cort-y2').val(c.y2);
}


$j(document).ready(function(){
    $j(function(){
        $j('#usertImage').Jcrop({
            onChange: exibePreview,
            onSelect: exibePreview,
            aspectRatio: 1
        });
    });
});