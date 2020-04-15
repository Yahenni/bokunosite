document.getElementById("captcha-text").value=""
var hashkey = null;
var get_captcha = function() {
	var jqxhr = $.ajax("/api/captcha/", {
		contentType: 'application/json',
		type: 'GET',
	})
	.done(function(data) {
		$("#captcha-img").attr("src", data.image_url);
		hashkey = data.key;
	})
	.fail(function() {
		console.log("Error geting captcha")
	});
};

var refresh_captcha = function () {
	var jqxhr = $.ajax("/api/captcha/" + hashkey, {
		contentType: 'application/json',
		type: 'GET',
	})
	.done(function(data) {
		$("#captcha-img").attr("src", data.image_url);
		hashkey = data.key;
	})
	.fail(function() {
		console.log("Error refreshing catcha");
	});
};

get_captcha();

var validation_captcha = function () {
	var $form = document.getElementById("captcha-text")
	var $feedback = document.getElementById("captcha-feedback")
	if (! $form.checkValidity()) {
		$form.classList.add("is-invalid")
		if ( $form.value.length == 0 ) {
			$feedback.innerText="Пожалуйста, введите капчу"
		} else if ( $form.value.length != 6) {
			$feedback.innerText="Капча состоит из 6 символов"
		};
	};
	return $form.checkValidity();
};

validation_captcha();

$("#captcha-validate").click(function () {
	if (! validation_captcha()) {return}
	var text = $("#captcha-text").val();
	$.ajax("/api/captcha/" + hashkey + "/" + text, {
		contentType: 'application/json',
		type: 'GET',
	})
	.done(function() {
		console.log("Captcha validated!");
		document.getElementById("captcha-text").classList.remove("is-invalid");
		document.getElementById("captcha-text").classList.add("is-valid");
		document.getElementById("captcha-text").readOnly=true;
		document.getElementById("captcha-refresh").disabled=true;
		document.getElementById("captcha-validate").disabled=true;
		document.getElementById("hash").value=hashkey;
	})
	.fail(function() {
		console.log("Captcha NOT validated!");
		document.getElementById("captcha-feedback").innerText="Качпа решена не верно. Повторите попытку";
		document.getElementById("captcha-text").value=""
		refresh_captcha();
	});
});

$("#captcha-refresh").click(function () {
	var text = $("#captcha-text").val();
	$.ajax("/api/captcha/" + hashkey + "/", {
		contentType: 'application/json',
		type: 'GET',
	})
	.done(function() {
		console.log("Captcha refreshed");
	})
	.fail(function() {
		console.log("Captcha not refreshed");
		refresh_captcha();
	});
});
