$(document).ready(function() {
	$(".modulelist").on('click',"button.mymodule",function(){
		var action_type = $(this).data("modtype");
		var module_id = $(this).data("modid");
		$.get($(location).attr('href'),
			{
				'action_type': action_type,
				'module_id': module_id
			},
			function(response) {
				$('.modulelist').html(response);
			})
	});
});