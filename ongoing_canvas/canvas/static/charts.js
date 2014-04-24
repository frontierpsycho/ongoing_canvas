function addHorizontalBarChart(paper, feelingCounts, feelingColours, feelingLegend, chartName) {

	var fin = function () {
		if (!this.hasOwnProperty("flag")) {
			this.flag = paper.popup(this.bar.x, this.bar.y, this.bar.value || "0").insertBefore(this);
		}
		this.flag.attr("opacity", 1);
	};
	var fout = function () {
		this.flag.animate({opacity: 0}, 300);
	};

	var chart_height = 300;
	var chart_width = 760;
	var chart_x = 960 - chart_width - 100;

	var hbarchart = paper.hbarchart(chart_x, 40, chart_width, chart_height, feelingCounts, { colors: feelingColours })
		.hover(fin, fout);

	var textattr = {
		"font-size": 18,
		"text-anchor": "end"
	};

	if (feelingLegend) {
		var bbox = hbarchart.getBBox();
		var y = bbox.y + textattr['font-size']/2;
		var increment = chart_height/feelingLegend.length - 1.9;
		for(var i = 0; i < feelingLegend.length; i++) {
			paper.text(bbox.x - 10, y, feelingLegend[i]).attr(textattr);
			y += increment;
		}
	}

	paper.text(bbox.x + (chart_width/2), 10, chartName).attr({
		"font-size": 25,
		"font-weight": "bold"
	});
}
