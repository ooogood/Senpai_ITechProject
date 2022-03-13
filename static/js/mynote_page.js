$(document).ready(function() {
	$(".notelist").on('click',"button.delete_note",function(){
		var note_id = $(this).data("noteid");
		$.get($(location).attr('href'),
			{
				'noteid': note_id
			},
			function(response) {
				$('.notelist').html(response);
			})
	});
});