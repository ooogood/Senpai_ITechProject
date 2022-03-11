$(document).ready(function() {
	$("#btn_sort_lik").click(function(){
		$.get($(location).attr('href'),
			{
				sort_type: 'lik'
			},
			function(response) {
				$('.content.links').html(response);
			})
	});
	$("#btn_sort_cmt").click(function(){
		$.get($(location).attr('href'),
			{
				sort_type: 'cmt'
			},
			function(response) {
				$('.content.links').html(response);
			})
	});
	$("#btn_sort_new").click(function(){
		$.get($(location).attr('href'),
			{
				sort_type: 'new'
			},
			function(response) {
				$('.content.links').html(response);
			})
	});
	$("#btn_sort_old").click(function(){
		$.get($(location).attr('href'),
			{
				sort_type: 'old'
			},
			function(response) {
				$('.content.links').html(response);
			})
	});
});