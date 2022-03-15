$(document).ready(function() {
	$(".content.frame").on('click',"div.module",function(){
		var action_type = $(this).data("modtype");
		var module_id = $(this).data("modid");
		/**
		 * Seperately refresh two blocks otherwise beautiful scroll might go wrong
		 */
		// refresh user module block (do add or delete module action in this response)
		$.get($(location).attr('href'),
			{
				'action_type': action_type,
				'module_id': module_id,
				'block': 'user'
			},
			function(response) {
				$('.user_modules').html(response);
				// refresh other module block after user block is refreshed
				// to prevent the other module refresh before the database is updated
				$.get($(location).attr('href'),
					{
						'block': 'other'
					},
					function(response) {
						$('.other_modules').html(response);
					})
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