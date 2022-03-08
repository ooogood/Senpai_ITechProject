$(document).ready(function() {
	$("#search-input").keyup(function(){
		let query = $(this).val();
		$.get($(location).attr('href'),
			{
				'search': query
			},
			function(response) {
				$('.home_modules').html(response);
			})
	});
});