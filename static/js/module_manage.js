$(document).ready(function() {
	$(".modulelist").on('click',"button.delete",function(){
		var action = 'delete';
		var module_id = $(this).data("modid");
		$.get($(location).attr('href'),
			{
				'action_type': action,
				'module_id': module_id,
			},
			function(response) {
				$('.modulelist').html(response);
			});
	});

	$(".add_module_frame").on('click',"button.add_module",function(){
		var action = 'add';
		var txt = $("#txt_module").val();
		$.get($(location).attr('href'),
			{
				action_type: action,
				module_name: txt,
			},
			function(response) {
				$("#txt_module").val("");
				$('.modulelist').html(response);
			});
	});
});