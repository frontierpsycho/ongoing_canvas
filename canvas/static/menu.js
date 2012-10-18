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

$("#menuForm").submit(function(evt) {
	evt.preventDefault();
	var checked_nodes = $("#feelingtree").jstree("get_checked", null, false);
	var array_for_submission = $(this).serializeArray();
	$.map(checked_nodes, function(node, index) {
		var checkbox_id = $(node).children("input:checkbox").filter(":first").val();//.attr("id");
		array_for_submission.push({name: "feeling", value: checkbox_id});
	});

	var url = "?"+$.param(array_for_submission);

	window.location = url;
});
