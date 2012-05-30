
$(document).ready(function(){		
	$(".next_arrow").live("click",function(){
		$(this).parent().find(".pre_arrow").show();
		var pic_index = $(this).parent().find('.pic-scroll').attr('src-index');
		var pic_str = $(this).parent().find('.pic-scroll').attr('all-src');
		var src_prefix = $(this).parent().find('.pic-scroll').attr('src-prefix');
		//var pic_arr = pic_str.split(';');
		var src_objects = $.parseJSON(pic_str);
		var src_obj_path = [];
		var src_obj_size = [];
		$.each(src_objects, function(index, value) {
			src_obj_path[index] = src_prefix+value.name; 
			src_obj_size[index] = value.is_over_16_9;
		})

		if(pic_index < src_obj_path.length-1){
			pic_index++;
  		    $(this).parent().find('.pic-scroll').attr('src-index',pic_index);
				if(src_obj_size[pic_index]){
					$(this).parent().find("img").attr({src:src_obj_path[pic_index],width:"160"});
					$(this).parent().find("img").removeAttr('height');
				}else{	
					$(this).parent().find("img").attr({src:src_obj_path[pic_index],height:"90"});
					$(this).parent().find("img").removeAttr('width');
				}	
		}
		if(pic_index ==src_obj_path.length-1){
			$(this).parent().find(".next_arrow").hide();
		}
	});
		
	$(".pre_arrow").live("click",function(){
		$(this).parent().find(".next_arrow").show();
		var pic_index = $(this).parent().find('.pic-scroll').attr('src-index');
		var pic_str = $(this).parent().find('.pic-scroll').attr('all-src');
		var src_prefix = $(this).parent().find('.pic-scroll').attr('src-prefix');
		var src_objects = $.parseJSON(pic_str);
		var src_obj_path = [];
		var src_obj_size = [];
		$.each(src_objects, function(index, value) {
			src_obj_path[index] = src_prefix+value.name; 
			src_obj_size[index] = value.is_over_16_9;
		})

		if(pic_index >0){			
			pic_index--;
			$(this).parent().find('.pic-scroll').attr('src-index',pic_index);
			if(src_obj_size[pic_index]){
				$(this).parent().find("img").attr({src:src_obj_path[pic_index],width:"160"});
				$(this).parent().find("img").removeAttr('height');
			}else{
				$(this).parent().find("img").attr({src:src_obj_path[pic_index],height:"90"});
				$(this).parent().find("img").removeAttr('width');
			}	
		}
		if(pic_index == 0){
			$(this).parent().find(".pre_arrow").hide();
		}
		
	});
});