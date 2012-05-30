$(function() {
	var num_pages=$("#num_pages").val();
	$("#current_page").val("1");
	$("#load_more_button").click(function(e){
		loadMore(e.pageY);
		return false;
    });
	
	function loadMore(y){
		var page=parseInt($("#current_page").val())+1;
		$("#current_page").val(page);
        $("#load_more_contents").load('/sharings/load_more/?page='+page,
        function(e){
        	$('#load_more_contents').find('#prompt_message').show();
        	if(page==num_pages){
        		$('#load_more_button').hide();
        	}
        	$('#append_more_contents').append($('#load_more_contents').children());
    		var position = $(".hide.alert-message").last().offset().top-500;
    		$('html, body').scrollTop(position);
        });
	}
	
	$(window).scroll(function(){
		if(($(document).height()==$(document).scrollTop() + $(window).height())&&($("#current_page").val()<num_pages)) {
			loadMore();
		}
	}); 
});