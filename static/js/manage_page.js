$(document).ready(function() {
	$(".modules").on('click',"div.delete",function(){
		var action = 'delete';
		var module_id = $(this).data("modid");
		$.get($(location).attr('href'),
			{
				'action_type': action,
				'module_id': module_id,
			},
			function(response) {
				$('.modules').html(response);
			});
	});

	$(".add_module_frame").on('click',"div.add_module",function(){
		var action = 'add';
		var txt = $("#txt_module").val();
		$.get($(location).attr('href'),
			{
				'action_type': action,
				'module_name': txt,
			},
			function(response) {
				$("#txt_module").val("");
				$('.modules').html(response);
			});
	});

	// scroll beautify
	$('.modules').niceScroll({
		cursorcolor: 'white',
		cursorwidth: '12px',
		cursorborder:'none',
		autohidemode: 'leave',
		horizrailenabled:false,
		railpadding: { top: 96, right: 0, left: 0, bottom: 12 }
	});
});