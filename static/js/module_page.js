$(document).ready(function() {
	$("#sort").click(function(){
		let order = $("#sort p").text();

		if(order == "Most Likes"){

			$("#sort p").text("Most Comments");
			$.get($(location).attr('href'),
				{
					sort_type: 'cmt'
				},
				function(response) {
					$('.content.links').html(response);
			});

		}else if(order == "Most Comments"){

			$("#sort p").text("Newest");
			$.get($(location).attr('href'),
				{
					sort_type: 'new'
				},
				function(response) {
					$('.content.links').html(response);
			})

		}else if(order == "Newest"){

			$("#sort p").text("Oldest");
			$.get($(location).attr('href'),
				{
					sort_type: 'old'
				},
				function(response) {
					$('.content.links').html(response);
			})

		}else if(order == "Oldest"){

			$("#sort p").text("Most Likes");
			$.get($(location).attr('href'),
				{
					sort_type: 'lik'
				},
				function(response) {
					$('.content.links').html(response);
			})

		}
	});

	// scroll beautify
	$('.moduleframe').niceScroll({
		cursorcolor: 'white',
		cursorwidth: '12px',
		cursorborder:'none',
		autohidemode: 'leave',
		horizrailenabled:false,
		railpadding: { top: 96, right: 0, left: 0, bottom: 12 }
	});

	$('.noteframe').niceScroll({
		cursorcolor: 'white',
		cursorwidth: '12px',
		cursorborder:'none',
		autohidemode: 'leave',
		horizrailenabled:false,
		railpadding: { top: 96, right: 0, left: 0, bottom: 12 }
	});
});