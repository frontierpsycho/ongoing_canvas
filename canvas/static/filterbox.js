$(function() {
	$('#filterbox [id$="_Toggle"]').click(function() {
		var tokens = $(this).attr("id").split("_");
		tokens.pop();
		var toggleTarget = tokens.join("_");

		// get toggle button position to place dialog
		var position = $("#filterbox").offset();

		position.top = position.top + $("#filterbox").outerHeight();


		$("#"+toggleTarget).css({left: position.left, top: position.top }).slideToggle();
	});

	$("#submenus #feelingChoose button").click(function() {
		$("#filterboxForm").submit();
	});

	$("#filterboxForm").submit(function(evt) {
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

});

var buildMenu = function(treedata) {
	var tree = $.jstree._reference("#feelingtree");

	for(var i = 0; i < treedata.length; i++) {
		var treeNode = treedata[i];
		var category = treeNode.data.charAt(0).toUpperCase() + treeNode.data.substring(1);
		var categoryNode = $("td.catName:contains('"+category+"')");

		if(treeNode.hasOwnProperty('children')) {
			for(var j = treeNode.children.length-1; j >= 0 ; j--) {
				var child = treeNode.children[j];
				var checkboxId = "#"+child.attr.id;
				var elementToAdd = $.parseHTML('<td data-category="'+checkboxId+'">'+child.data+'</td>');

				categoryNode.after(elementToAdd);
				$(elementToAdd[0]).click(function(event) {
					var nodeId = $(this).data('category');
					if(tree.is_checked(nodeId)) {
						tree.uncheck_node(nodeId);
					} else {
						tree.check_node(nodeId);
					}
					$("#filterboxForm").submit();
				});
			}
		}

		categoryNode.click(function(event) {
			var nodeId = "#"+category+"_node";
			if(tree.is_checked(nodeId)) {
				tree.uncheck_node(nodeId);
			} else {
				tree.check_node(nodeId);
			}
			$("#filterboxForm").submit();
		});
	}
};
