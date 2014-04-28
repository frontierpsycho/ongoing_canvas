function addHorizontalBarChart(paper, counts, colours, legend, chartName) {

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

	var hbarchart = paper.hbarchart(chart_x, 40, chart_width, chart_height, counts, { colors: colours })
		.hover(fin, fout);

	var bbox = hbarchart.getBBox();

	paper.text(bbox.x + (chart_width/2), 10, chartName).attr({
		"font-size": 25,
		"font-weight": "bold"
	});

	if (legend) {
		addLegend(paper, legend, hbarchart, chart_height);
	}
}

function addLegend(paper, legend, chart, chart_height) {
	var textattr = {
		"font-size": 18,
		"text-anchor": "end"
	};

	var bbox = chart.getBBox();
	var y = bbox.y + textattr['font-size']/2;
	var increment = chart_height/legend.length - 1.8;

	var shapes = isPath(legend[0]);

	for(var i = 0; i < legend.length; i++) {
		if (shapes) {
			paper.path(legend[i]).transform("t" + (bbox.x - 60) + "," + y );
		} else {
			paper.text(bbox.x - 10, y, legend[i]).attr(textattr);
		}
		y += increment;
	}
}

function isPath(string) {
	var re = /M[-.,\w]*z/g;
	return re.test(string);
}
