/**
 * tab switcher loading data by ajax
 */
$(function () {
	var tabs = $('#tabs li');
	tabs.click(function(e){
		e.preventDefault();
		var tabIndex = tabs.index(this);
		tabs.filter('.active').removeClass('active');
		tabs.eq(tabIndex).addClass('active');
		var tabPanel = $('#sharings-list-content>.tab-pane');
		tabPanel.filter('.active').removeClass('active');
		var selectTabPanel = tabPanel.eq(tabIndex);
		selectTabPanel.addClass('active');
        if(!selectTabPanel.html().trim()){
        	selectTabPanel.load($(this).children().get(0).href);
        }
	});
});

/**
 * detail panel operation: show and hide
 */
$(function(){
	var dashboardPanel = $('body>.container>.row>.dashboard');
	var detailPanel = $('#details-pane-outer div.details-pane');
	var moreSwitcher = $('#sharings-list-content div.more');
	
	
	moreSwitcher.live('click', function(e){
		if(detailPanel.hasClass('js-details-pane-hidden')){
			showDetailPanel();
		}else{
			hideDetailPanel();
		}
	});
	
	$('body>.container #details-pane-outer .pane-toolbar a').click(function(e){
		hideDetailPanel();
	});
//	
//	$('.js-stream-item').click(function(e){
//		moreSwitcher.click();
//	});
	
	function showDetailPanel(){
		dashboardPanel.hide();
		moreSwitcher.parent().addClass('focused-stream-item');
//		$('.js-stream-item').addClass('focused-stream-item');
		detailPanel.removeClass('js-details-pane-hidden');
		detailPanel.addClass('js-details-pane-shown');
		var sharingId = moreSwitcher.parent().find('input[type="hidden"][name="sharing_id"]').val();
		$('#comments-container .js-load-comments', detailPanel).load('/sharings/' + sharingId + '/comments/');
	}
	
	function hideDetailPanel(){
		dashboardPanel.show();
		moreSwitcher.parent().removeClass('focused-stream-item');
//		$('.js-stream-item').removeClass('focused-stream-item');
		detailPanel.removeClass('js-details-pane-shown');
		detailPanel.addClass('js-details-pane-hidden');
	}
});

