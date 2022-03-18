$(document).ready(function() {
	$("#sort").click(function(){
		let order = $("#sort p").text();

		if(order == "Most Likes"){

			$("#sort p").text("Most Comments");
			$.get($(location).attr('href'),
				{
					action: 'sort',
					sort_type: 'cmt'
				},
				function(response) {
					$('.content.noteframe').html(response);
			});

		}else if(order == "Most Comments"){

			$("#sort p").text("Newest");
			$.get($(location).attr('href'),
				{
					action: 'sort',
					sort_type: 'new'
				},
				function(response) {
					$('.content.noteframe').html(response);
			})

		}else if(order == "Newest"){

			$("#sort p").text("Oldest");
			$.get($(location).attr('href'),
				{
					action: 'sort',
					sort_type: 'old'
				},
				function(response) {
					$('.content.noteframe').html(response);
			})

		}else if(order == "Oldest"){

			$("#sort p").text("Most Likes");
			$.get($(location).attr('href'),
				{
					action: 'sort',
					sort_type: 'lik'
				},
				function(response) {
					$('.content.noteframe').html(response);
			})

		}
	});
	
	// click like module button
	$("#like").click(function(){
		$.get($(location).attr('href'),
			{
				action: 'like',
			},
			function(response) {
				// erase the like button
				$("#like p").animate({'opacity': '0'}, 500, function(){
					$("#like p").text("");
					$("#like p").css({'opacity': '1', 'background-position': 'center 45px', 'background-size': '20px 18px', 'background-repeat': 'no-repeat', 'background-image': "url('/static/img/confirm_icon.webp')"});
					$("#like p").animate({'top': '-36px'}, 500, function(){
						$("#like p").animate({'top': '-36px'}, 700, function(){
							$("#like").animate({'opacity': '0'}, 300, function(){
								$("#like p").css({'display': 'none'})
							});
						});
					});
				})
		})
	});

	// scroll beautify
	$('.moduleframe, .noteframe').niceScroll({
		cursorcolor: 'white',
		cursorwidth: '12px',
		cursorborder:'none',
		autohidemode: 'leave',
		horizrailenabled:false,
		railpadding: { top: 96, right: 0, left: 0, bottom: 12 }
	});
});