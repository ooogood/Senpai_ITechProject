$(document).ready(function() {
	$(".component.like").click(function(){
		let url = $(location).attr('href') + '/like_clicked';
		$.get(url,
			{},
			function(response) {
				$('.component.like').html(response);
			})
	});

	$(".button.download").click(function(){
		$("#download_form").submit();
	});

	$("#btn_add_comment").click(function(){
		let txt = $("#txt_comment").val();
		$.get($(location).attr('href'),
			{
				txt: txt
			},
			function(response) {
				$("#txt_comment").val("");
				$('.commentsframe').html(response);
			});
	});

	// scroll beautify
	$('.component.add_comment').niceScroll({
		cursorcolor: 'white',
		cursorwidth: '12px',
		cursorborder:'none',
		autohidemode: false,
		horizrailenabled: false,
		railpadding: { top: 0, right: 6, left: 0, bottom: 0 }
	});

	$('.commentsframe').niceScroll({
		cursorcolor: 'white',
		cursorwidth: '12px',
		cursorborder:'none',
		autohidemode: 'leave',
		horizrailenabled: false,
	});
});