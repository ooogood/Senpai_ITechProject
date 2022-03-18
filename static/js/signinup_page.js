$(document).ready(function() {
	$(".switch.signup").click(function(){
		$(".sign.in").animate({top:'240px', left: '48px', right: '576px'}, 300);
		$("div.switch.signin").animate({opacity: '1'}, 300);
		$("p.switch.signin").animate({'font-size': '18'}, 300);
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

	$(".switch.signin").click(function(){
		$(".sign.up").animate({top:'240px', left: '576px', right: '48px'}, 300);
		$("div.switch.signup").animate({opacity: '1'}, 300);
		$("p.switch.signup").animate({'font-size': '18'}, 300);
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