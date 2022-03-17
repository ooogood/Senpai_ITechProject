$(document).ready(function() {
	$(".keygen").on('click',"#genkey_button",function(){
		$.get($(location).attr('href'),
			{
				'req': 'gen_admin_key'
			},
			function(response) {
				$('.adminkey').html(response);
			})
	});
});