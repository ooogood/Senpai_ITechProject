$(document).ready(function() {
	$(".content.preview.like_info").on('click',"#btn_like_note",function(){
		let url = $(location).attr('href') + '/like_clicked';
		$.get(url,
			{},
			function(response) {
				$('.content.preview.like_info').html(response);
			})
	});
	$("#btn_add_comment").click(function(){
		let txt = $("#txt_comment").val();
		$.get($(location).attr('href'),
			{
				txt: txt
			},
			function(response) {
				$("#txt_comment").val("add a comment...")
				$('.content.commentarea.commentpage').html(response);
			});
	});
});