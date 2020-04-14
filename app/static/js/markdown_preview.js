 $("#nav-profile-tab").click(function () {
	var jqxhr = $.ajax("/api/markdown", {
		contentType: 'application/json',
		type: 'POST',
		data: JSON.stringify({data: editor_for_data.getDoc().getValue()})
	})
	.done(function(data) {
		$("#preview-block").html(data.html);
	})
	.fail(function(){
		console.log("Can't load preview");
	});
});

