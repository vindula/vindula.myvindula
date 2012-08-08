$j = jQuery.noConflict();

$j(document).ready(function(){
	
	$j('#import-button').click(function () {
		
		$j(this).hide();
		$j('.imgLoader').show();
		
	});
	
	for(var i = 1; i <= $j('table.tableImport tbody tr').length; i++)
	{
		element = $j('table.tableImport tbody tr').eq(i)
		if (i % 2 != 0)
		  element.attr('class', 'cor1')
	}
});