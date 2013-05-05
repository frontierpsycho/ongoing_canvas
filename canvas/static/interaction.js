function add_interaction(element, id, colour) {
	// HACKISH add percentage sign after second and third value
	var colourParts = colour.split(',');
	colourParts[1] += "%";
	colourParts[2] = colourParts[2].substring(0,colourParts[2].length-1)+"%)";
	colour = colourParts.join(',');
	element.hover(
			function(e) {
				this.gl = this.glow({ color: "#CCC", width: 5 });
			},
			function(e) {
				this.gl.remove();
			})
	.click(function(e) {
		$('div#popup').css('background-color', colour).css('opacity', '0.9')
		.bPopup({
			contentContainer: ".content",
			loadUrl: '/canvas/feeling/'+id+'/', //Uses jQuery.load()
			loadCallback: function() {
				var interval;
				var textFill = function() {
					$("div#popup div.textfill").textfill( { maxFontPixels: 72 } );
					window.clearInterval(interval);
				}
				var textFillFunction = function(count) {
					return function() {
						if(count == 0 || $('div.textfill span:visible').length > 0) {
							textFill();
							return;
						}
						count -= 1;
					}
				};
				interval = setInterval(textFillFunction(100), 10);

				$("div#popup div#closeButton div.actualButton").click(function(event) {
					$("div#popup").bPopup().close();
				});
			},
			speed: 10,
			position: ['auto','auto'],
			positionStyle: 'fixed'
		});
	});
}
