$(document).ready(function() {
	$(".note_like_info").on('click',"#btn_like_note",function(){
		let url = $(location).attr('href') + '/like_clicked';
		$.get(url,
			{},
			function(response) {
				$('.note_like_info').html(response);
				console.log(response);
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
				$('.comments').html(response);
			});
	});
});