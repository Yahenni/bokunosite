var article_id = window.location.pathname.split("/")[3];
var token = null;

var get_token = function() {
	var jqxhr = $.ajax("/api/token/", {
		contentType: 'application/json',
		type: 'GET',
	})
	.done(function(data) {
		token = data.token;
		console.log("Token geted")
	})
	.fail(function() {
		console.log("Error getting token")
	});
};

get_token();
$("#delete_button").click(function () {
	$.ajax("/api/article/" + article_id + "/remove/", {
		contentType: 'application/json',
		type: 'POST',
		beforeSend: function(request) {
			console.log(token);
    			request.setRequestHeader("Authorization", "Bearer " + token);
		}
	})
	.done(function(data) {
		console.log("Article removed");
		window.location.pathname=window.location.pathname.split("/").slice(0, -1).join("/");
	})
	.fail(function(data) {
		console.log("Error removing")
	});
});
