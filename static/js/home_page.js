$(document).ready(function() {
	$(".navigation.input.search").keyup(function(){
		let query = $(this).val();
		$.get($(location).attr('href'),
			{
				'search': query
			},
			function(response) {
				$('.content.links').html(response);
			})
	});

	// scroll beautify
	$('.content.frame').niceScroll({
		cursorcolor: 'white',
		cursorwidth: '12px',
		cursorborder:'none',
		autohidemode: 'leave',
		horizrailenabled:false,
		railpadding: { top: 96, right: 0, left: 0, bottom: 12 }
	});
});