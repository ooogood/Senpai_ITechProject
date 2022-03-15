$(document).ready(function() {
	$(".content.frame").on('click',"div.module",function(){
		var action_type = $(this).data("modtype");
		var module_id = $(this).data("modid");
		$.get($(location).attr('href'),
			{
				'action_type': action_type,
				'module_id': module_id
			},
			function(response) {
				$('.content.frame').html(response);
			})
	});

	// scroll beautify
	$('.user_modules, .other_modules').niceScroll({
		cursorcolor: 'white',
		cursorwidth: '12px',
		cursorborder:'none',
		autohidemode: 'leave',
		horizrailenabled:false,
		railpadding: { top: 96, right: 0, left: 0, bottom: 12 }
	});
});