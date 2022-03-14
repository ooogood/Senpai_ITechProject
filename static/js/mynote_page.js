$(document).ready(function() {
	$(".notesframe").on('click',".delete_note",function(){
		var note_id = $(this).data("noteid");
		$.get($(location).attr('href'),
			{
				'noteid': note_id
			},
			function(response) {
				$('.notesframe').html(response);
			})
	});

	// scroll beautify
	$('.notesframe').niceScroll({
		cursorcolor: 'white',
		cursorwidth: '12px',
		cursorborder:'none',
		autohidemode: 'leave',
		horizrailenabled: false,
		railpadding: { top: 96, right: 0, left: 0, bottom: 12 }
	});
});