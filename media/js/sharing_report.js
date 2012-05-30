google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(function(){
	$('.keyword-percentage-recent').click(function(){
		keywords=[
	        ['Coca-Cola', 2000],
	        ['Pepsi', 1500], 
	        ['KangShiFu', 1400],
	        ['RedBull', 1300],
	        ['Nestle', 1000],
	        ['TongYi',700],
	        ['Wahaha', 600],
	        ['WangLaoJi', 500]
	      ];
		drawChart(keywords);
		return false;
	});
	
	
	$('.keyword-percentage').click(function(){
		$.post("/sharings/keywords_analysis/",
			{brand:$(this).parents('tr').find('.brand').text()},
			function(data){
				var keywords=[];
				$.each($.parseJSON(data), function(key, value) {
						var keyval=[key,value];
						keywords.push(keyval);
					});
				drawChart(keywords);
			});
		return false;
	});
	
	
	function drawChart(keywords){
		var data = new google.visualization.DataTable();
		data.addColumn('string', 'Topping');
		data.addColumn('number', 'Slices');
		data.addRows(keywords);
		var options = {'title':'Keywords in Related Message:','width':320,'height':180};
		var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
		chart.draw(data, options);
	}
	
});
	

