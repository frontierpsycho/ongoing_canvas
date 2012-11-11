function add_interaction(element, id) {
	element.hover(
			function(e) {
				this.gl = this.glow({ color: "#CCC", width: 5 });
			},
			function(e) {
				this.gl.remove();
			})
	.click(function(e) {
		$('#popup').bPopup({
			contentContainer: ".content",
			loadUrl: '/canvas/feeling/'+id+'/', //Uses jQuery.load()
			position: ['auto','auto'],
			positionStyle: 'fixed'
		});
	});
}
