$(document).ready(function() {

	$(".login.button.submit").click(function(){
		$.ajax({
			type: "POST",
			dataType: "json",
			url: $(location).attr('href'),
			data: $('#login_form').serialize()+"&type=signin",
			success: function (response) {
				response = Object.values(response);
				if(response[0]=='success'){
					window.location.href="/senpai";
				}else{
					$(".loginerr").html("Error: " + response[0]);
				}
			}
		})
	});

	$("input.login.password").keydown(function(e){
		if(e.which == 13){
			$.ajax({
				type: "POST",
				dataType: "json",
				url: $(location).attr('href'),
				data: $('#login_form').serialize()+"&type=signin",
				success: function (response) {
					response = Object.values(response);
					if(response[0]=='success'){
						window.location.href="/senpai";
					}else{
						$(".loginerr").html("Error: " + response[0]);
					}
				}
			})
		}
	});

	$(".register.button.submit").click(function(){
		$.ajax({
			type: "POST",
			dataType: "json",
			url: $(location).attr('href'),
			data: $('#user_form').serialize()+"&type=signup",
			success: function (response) {
				response = Object.values(response);
				if(response[0]=='success'){
					window.location.href="/senpai";
				}else{
					$(".registererr").html("Error: " + response[0]);
				}
			}
		})
	});

	$("input.register.password, #id_admin_key").keydown(function(e){
		if(e.which == 13){
			$.ajax({
				type: "POST",
				dataType: "json",
				url: $(location).attr('href'),
				data: $('#user_form').serialize()+"&type=signup",
				success: function (response) {
					response = Object.values(response);
					if(response[0]=='success'){
						window.location.href="/senpai";
					}else{
						$(".registererr").html("Error: " + response[0]);
					}
				}
			})
		}
	});

	$(".sign.up").click(function(){
		$(".sign.in").css({'cursor': 'pointer'});
		$(".sign.in").animate({top:'240px', left: '48px', right: '576px'}, 300);
		$("div.switch.signin").animate({opacity: '1'}, 300);
		$("p.switch.signin").animate({'font-size': '18'}, 300);
		$(".sign.up").css({'cursor': 'default'});
		$(".sign.up").animate({top:'36px', left: '540px', right: '0px'}, 300);
		$("div.switch.signup").animate({opacity: '0'}, 300);
		$("p.switch.signup").animate({'font-size': '36'}, 300);
		$(".forms").animate({'left': '-336'}, 300);
		$("#login_form").animate({opacity: '0'}, 300, function(){
			$(this).css({'display': 'none'});
		});
		$("#user_form").css({'display':'block'});
		$("#user_form").animate({opacity: '1'}, 300);
	})

	$(".sign.in").click(function(){
		$(".sign.up").css({'cursor': 'pointer'});
		$(".sign.up").animate({top:'240px', left: '576px', right: '48px'}, 300);
		$("div.switch.signup").animate({opacity: '1'}, 300);
		$("p.switch.signup").animate({'font-size': '18'}, 300);
		$(".sign.in").css({'cursor': 'default'});
		$(".sign.in").animate({top:'36px', left: '0px', right: '540px'}, 300);
		$("div.switch.signin").animate({opacity: '0'}, 300);
		$("p.switch.signin").animate({'font-size': '36'}, 300);
		$(".forms").animate({'left': '0'}, 300);
		$("#user_form").animate({opacity: '0'}, 300, function(){
			$(this).css({'display': 'none'});
		});
		$("#login_form").css({'display':'block'});
		$("#login_form").animate({opacity: '1'}, 300);
	})
});