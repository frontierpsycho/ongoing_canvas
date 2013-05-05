function add_interaction(element, id, colour) {
	// HACKISH add percentage sign after second and third value
	colourParts = colour.split(',');
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
                $("#popup div.textfill").textfill( { maxFontPixels: 72 } );
                $("#popup div#actualButton").click(function(event) {
                    $("div#popup").bPopup().close();
                });
		    },
			position: ['auto','auto'],
			positionStyle: 'fixed'
		});
	});
}
