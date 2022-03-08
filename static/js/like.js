$(document).ready(function() {
	$("#like").click(function(){
		var note = $(this).data("note")
		$.get($(location).attr('href'),
			{
				'note_id': note
			},
	});
});