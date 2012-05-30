$(document).ready(function() {
	$.formValidator.initConfig({
		formid : "regist_form",
		onerror : function(msg) {
			return false
		}	
	});
	
	$("#id_username").formValidator({
		onshow : "请输入用户名",
		onfocus : "用户名至少3个字符,最多10个字符",
		oncorrect : "该用户名可以注册"
	}).inputValidator({
		min : 3,
		max : 10,
		onerror : "你输入的用户名非法,请确认"
	}).regexValidator({
		regexp : "username",
		datatype : "enum",
		onerror : "用户名格式不正确"
	});
//	.ajaxValidator({ //ajax 验证	
//	    type : "post",
//		url : "/regist/",
//		data :{registname:$('#id_username').val()},
//		success : function(data){	
//			alert(data);
//            if( data == "username had existed" )
//			{
//                return true;
//			}
//            else
//			{
//                return false;
//			}
//		},
//		buttons: $("#regist_submit"),
//		onerror : "该用户名不可用，请更换用户名"
//	});
	
//	var validator_flag = false;
//	$('#id_username').blur(function(){
//		$.post("/regist/",{registname:$('#id_username').val()},
//			 function(data){
//				//alert(data);
//				//alert($.parseJSON(data));
//				if(data=='existed'){
//					//alert("用户名被占用");
//					$("#id_usernameTip").attr("class","onError");
//					$('#id_usernameTip').text('用户名被占用');
//					validator_flag = true;
//				}
//			});
//			//return true;
//	});
//
//	
//	$('#regist_form').submit(function(){
//		if(validator_flag){
//			$("#id_usernameTip").attr("class","onError");
//    		$('#id_usernameTip').text('用户名被占用');
//			return false;
//		}
//		$("#id_usernameTip").attr("class","onCorrect");
//		$('#id_usernameTip').text('该用户名可以注册');
//		return true;
//	});
	
	$("#id_password").formValidator({
		onshow : "请输入密码",
		onfocus : "密码至少6位",
		oncorrect : "密码合法"
	}).inputValidator({
		min : 6,
		empty : {
			leftempty : false,
			rightempty : false,
			emptyerror : "密码两边不能有空符号"
		},
		onerror : "密码至少6位,请确认"
	});
	
	$("#id_confirm").formValidator({
		onshow : "请输入重复密码",
		onfocus : "两次密码必须一致哦",
		oncorrect : "密码一致"
	}).inputValidator({
		min : 6,
		empty : {
			leftempty : false,
			rightempty : false,
			emptyerror : "重复密码两边不能有空符号"
		},
		onerror : "重复密码不能为空,请确认"
	}).compareValidator({
		desid : "id_password",
		operateor : "=",
		onerror : "2次密码不一致,请确认"
	});
	
	$("#id_email").formValidator({
		onshow : "请输入邮箱",
		onfocus : "邮箱6-30个字符",
		oncorrect : "该邮箱可用"
	}).inputValidator({
		min : 6,
		max : 30,
		onerror : "你输入的邮箱长度非法,请确认"
	}).regexValidator({
		regexp : "^([\\w-.]+)@(([[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.)|(([\\w-]+.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(]?)$",
		onerror : "你输入的邮箱格式不正确"
	});

});