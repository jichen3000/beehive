/**
 * Comment add, show.
 */
$(function(){
	/**
	 * click event about showing comment form
	 */
	$("a.publish_comment_show").click(function(){
		$(this).next().show();
		$(this).hide();
	});
	
	/**
	 * comment form submit when adding comment
	 */
	$("form").submit(function(event){
		event.preventDefault(); 
		var $form = $( this ), 
			sharingId = $form.find('input[type="hidden"]').val(),
			commentsWrapDivId = "comments-" + sharingId,
			commentContent = $form.find('textarea[name="form_commentContent"]').val(),
			url = $form.attr('action');
		$.post(url, {commentContent: commentContent},
		    function(data) {
				var responseData = $.parseJSON(data);
				var comment = responseData[0];
				var author = responseData[1];
				var newCommentHtml = $("#sharing_comment_template").clone();
				var tbody = $("#" + commentsWrapDivId).find('tbody');
				tbody.children().last().after(newCommentHtml);
				newCommentHtml.find("tr").attr("id", "sharing_comment" + comment.pk);
				newCommentHtml.find("td").eq(0).text(comment.pk);
				newCommentHtml.find("div span:first").text(comment.fields.content);
				newCommentHtml.find("div a").text(author.fields.username);
				newCommentHtml.find("div span.last").text(comment.fields.created);
				newCommentHtml.show("slow");
				$form.find('textarea[name="form_commentContent"]').val('')
				$form.hide();
				$form.prev().show();
		    }
		);
	});
	
	/**
	 * key event when inputting content for comment   
	 */
	$('textarea[name="form_commentContent"]').keyup(function(){
		var submitBtn = $('input[name="form_comment_submit"]');
		if($(this).val() == ""){
			submitBtn.attr("disabled", "disabled");
		}else{
			submitBtn.removeAttr("disabled");
		}
		$('span[name="left_comment_count"]').text(200 - $(this).val().length);
	}).keyup();
});

/**
 * vote and follow
 */
$(function(){
	var voteAndFollowHandler = [];
	voteAndFollowHandler[0] = function(a){//vote up handler
		a.removeClass();
		a.addClass("vote-up-on disabled");
		a.parent().find('a').eq(1).addClass("disabled");
	};
	
	voteAndFollowHandler[1] = function(a){//vote down handler
		a.removeClass();
		a.addClass("vote-down-on disabled");
		a.parent().find('a').eq(0).addClass("disabled");
	};
	
	voteAndFollowHandler[2] = function(a){//follow handler
		a.toggleClass('star-on');
	};
	
	var spanClassPrefixes = ["j-vote-up-span-", 'j-vote-down-span-', 'j-follow-span-'];
	
	$('.vote-follow-div a').click(function(event){
		event.preventDefault(); 
		var a = $(this);
		if(a.hasClass('disabled')){
			return;
		}
		var sharingId = a.siblings('input[type="hidden"]').attr("value");
		var btnIndex = a.parent().find('a').index(this);
		voteAndFollowHandler[btnIndex](a);
		$.post(a.attr('href'), function(data){
			var responseData = $.parseJSON(data);
			a.parent().find("." + spanClassPrefixes[btnIndex] + sharingId).text(responseData.count);
		});
	});
});