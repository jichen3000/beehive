$(document).ready(function() {
	$('#id_content').keyup(function() {
		$('#preview_content').text($(this).val());
		if ($(this).val().length < 21) {
			$('#id_title').val($(this).val());
			$('#preview_title').text($('#id_title').val());
		} else {
			$('#id_title').val($(this).val().substring(0, 21));
			$('#preview_title').text($('#id_title').val());
		}
	}).keyup();

	$('#id_title').keyup(function() {
		$('#preview_title').text($(this).val());
		if ($(this).val().length != 0) {
			$('#id_content').unbind('keyup');
		}
		$('#id_content').keyup(function() {
			$('#preview_content').text($(this).val());
		});
	});
	var changeable=false;
	$('.changeable').live("change",function(){
		changeable=true;
	});
	

	$('#id_tags').keyup(function() {
		var tagValue = $(this).val();
		if(tagValue){
			$('#preview_tags').text(tagValue);
			$('#preview_tags').show();
		}else{
			$('#preview_tags').hide();
		}
	}).keyup();

	
	$('#id_file').live("change",function() {
		var obj=$(this).parents(".clearfix");
        $(this).upload('/sharings/medias/auto_save/', $('#add_sharing_form').serialize(), function(res) {
            var filename = res['filename'];
            var sharingid = res['sharingid'];
            var mediafileid=res['mediafileid'];
            var aspectratio=res['aspectratio'];
            $("#id_sharingid").val(sharingid);
            var appendimg=$("#image_preview_template").clone();
            appendimg.attr('id',mediafileid+'_image');
            appendimg.attr('src','/media/'+filename);
            if(aspectratio){
            	appendimg.attr('width','160');
            }else{
            	appendimg.attr('height','90');
            }
            appendimg.show();
            $("#preview_image").append(appendimg);
    
            
            var count=$("img[name='mediafile']").length;
            if((obj.next().find("#id_file").length==0)&&count<6){
            	var filehtml=$("#file_input_template").clone().find("input").attr({ value: '' }).end();
            	obj.after(filehtml);
            	filehtml.show();
            }else if(count==6){
            	obj.after($("#file_input_template").clone().attr({id:'file_display'}).find("input").attr({ value: '' }).end());
            }
            filename=filename.substring(filename.lastIndexOf('/')+1);
            var showfilenamehtml=$("#filename_preview_template").clone();
            showfilenamehtml.find("span").text("Filename: "+filename);
            showfilenamehtml.find("#id_mediafile").val(mediafileid);
            obj.after(showfilenamehtml);
            showfilenamehtml.show();
            obj.remove();
    }, 'json');
});
	
	
	$('#delete_file').live("click",function(){
		$("#file_display").show();
		var fileid=$(this).next().val();
		$.post("/sharings/ajax_delete_mediafile/",{mediafileid:fileid});
		$(this).parents(".clearfix").remove();
		$('#'+fileid+'_image').remove();
		if ($('#preview_image').find("img").length==0){
			$('#preview_image').text('');
		}
	});
	
	
	setInterval(function(){
			var title=$('#id_title').val();
			var content=$("#id_content").val();
			var file=$('#id_file').val();
			var tags=$("#id_tags").val();
			if((title!=''||content!=''||file!=''||tags!='')&&changeable){
				ajax_save_sharing();
			}
		}
	, 30000);
	

	$('#sharing_submit').click(function() {
		var is_validated=true; 
		if($('#id_title').val()==""){
			alert("Title is null");
			is_validated=false;
		}else if (funcCheckLength($('#id_title').val())>21){
			alert("Title is two long");
			is_validated=false;
		}if($('#id_content').val()==""){
			alert("Content is null");
			is_validated=false;
		}else if (funCheckLength($('#id_content').val().length)>200){
			alert("Content is two long");
			is_validated=false;
		}
		if (!is_validated){
			$('#add_sharing_form').submit(function(e) {
				e.preventDefault();
			});
		}
	});
	
	function funcCheckLength(strTemp) {
		var i, sum;
		sum = 0;
		for (i = 0; i < strTemp.length; i++) {
			if ((strTemp.charCodeAt(i) >= 0) && (strTemp.charCodeAt(i) <= 255))
				sum = sum + 1;
			else
				sum = sum + 2;
		}
		return sum;
	}
	
	function ajax_save_sharing(){
		$.post("/sharings/ajax_add_sharing/",$('#add_sharing_form').serialize(),function(data){
			$("#id_sharingid").val(data);
			$("#auto_save_p").text("Your Sharing has been saved");
			setInterval(function(){
				$("#auto_save_p").text(" ");
		    }, 1000);
		});
	}
});