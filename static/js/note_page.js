$(document).ready(function() {
	$(".content.preview.like_info").on('click',"#btn_like_note",function(){
		let url = $(location).attr('href') + '/like_clicked';
		$.get(url,
			{},
			function(response) {
				$('.content.preview.like_info').html(response);
			})
	});
	$(".content.commentarea.commentpage").on('click',"#prev_cmt_page",function(){
		$.get($(location).attr('href'),
			{
				page_num: parseInt( $("#cmt_page_num").text() ) - 1
			},
			function(response) {
				$('.content.commentarea.commentpage').html(response);
			})
	});
	$(".content.commentarea.commentpage").on('click',"#next_cmt_page",function(){

		console.log( parseInt( $("#cmt_page_num").text() ) + 1 )
		$.get($(location).attr('href'),
			{
				page_num: parseInt( $("#cmt_page_num").text() ) + 1
			},
			function(response) {
				$('.content.commentarea.commentpage').html(response);
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