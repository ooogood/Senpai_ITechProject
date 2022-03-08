$(document).ready(function() {
	$("#btn_add_comment").click(function(){
		let txt = $("#txt_comment").val()
		$.get($(location).attr('href'),
			{
				txt: txt
			},
			function(response) {
				$("#txt_comment").val("add a comment...")
				$('.comments').html(response);
			})
	});
});