$('#menu [id$="_Toggle"]').click(function() {
	var tokens = $(this).attr("id").split("_");
	tokens.pop();
	var toggleTarget = tokens.join("_");

	// get toggle button position to place menu
	var position = $(this).offset();

	position.top = position.top + $(this).outerHeight();

	var previous_pos = $("#"+toggleTarget).offset();
	
	$("#"+toggleTarget).css({left: position.left, top: position.top }).slideToggle();
});
