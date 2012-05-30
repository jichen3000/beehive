$(function(){
	$(document).ajaxSend(function(event, xhr, settings) {
	    function getCookie(name) {
	        var cookieValue = null;
	        if (document.cookie && document.cookie != '') {
	            var cookies = document.cookie.split(';');
	            for (var i = 0; i < cookies.length; i++) {
	                var cookie = jQuery.trim(cookies[i]);
	                // Does this cookie string begin with the name we want?
	                if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                    break;
	                }
	            }
	        }
	        return cookieValue;
	    }
	    function sameOrigin(url) {
	        // url could be relative or scheme relative or absolute
	        var host = document.location.host; // host + port
	        var protocol = document.location.protocol;
	        var sr_origin = '//' + host;
	        var origin = protocol + sr_origin;
	        // Allow absolute or scheme relative URLs to same origin
	        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	            // or any other URL that isn't scheme relative or absolute i.e relative.
	            !(/^(\/\/|http:|https:).*/.test(url));
	    }
	    function safeMethod(method) {
	        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	    }

	    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
	        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	    }
	});

	$('#topbar_unlogin').submit(function(event){
		event.preventDefault();
		var form = $(this),
			username = form.find('input[type="text"]').val(),
			password = form.find('input[type="password"]').val(),
			url = form.attr('action');
		$.post(url, 
				{username: username, password: password}, 
				function(data){
					form.hide();
					var loginedBar = $('#topbar_logined');
					loginedBar.children().first().find('a').text(data);
					loginedBar.show();
					window.location.reload();
				}
		);
	});
	
	$('#topbar_logined li:last').click(function(event){
		event.preventDefault();
		var li = $(this);
		$.get(li.find('a').attr('href'), 
			function(data){
				var loginedBar = $('#topbar_logined');
				loginedBar.children().first().find('a').text('');
				loginedBar.hide();
				$('#topbar_unlogin').show();
				window.location.reload();
			}
		);
	});
});