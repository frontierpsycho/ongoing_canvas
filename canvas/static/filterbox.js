$(function() {
	$('#filterbox [id$="_Toggle"]').click(function() {
		var tokens = $(this).attr("id").split("_");
		tokens.pop();
		var toggleTarget = tokens.join("_");

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

	$("#filterbox #closeButton div.actualButton").click(function(event) {
		collapseFilterBox();
	});

	$("#menu #openButton div.actualButton").click(function(event) {
		expandFilterBox();
	});
});

var buildFilterBox = function(treedata) {
	var tree = $.jstree._reference("#feelingtree");

	for(var i = 0; i < treedata.length; i++) {
		var treeNode = treedata[i];
		var category = treeNode.data.charAt(0).toUpperCase() + treeNode.data.substring(1);
		var categoryNode = $("td.catName:contains('"+category+"')");
		categoryNode.data('category', "#"+treeNode.attr.id);

		if(treeNode.hasOwnProperty('children')) {
			for(var j = treeNode.children.length-1; j >= 0 ; j--) {
				var child = treeNode.children[j];
				var checkboxId = "#"+child.attr.id;
				var elementToAdd = $.parseHTML('<td data-category="'+checkboxId+'">'+child.data+'</td>');

				categoryNode.after(elementToAdd);
				$(elementToAdd[0]).click($.proxy(function(event) {
					var nodeId = $(this.elementToAdd).data('category');
					tree.load_node(this.parentId, function() {}, function() {});
					if(tree.is_checked(nodeId)) {
						tree.uncheck_node(nodeId);
					} else {
						tree.check_node(nodeId);
					}
					$("#filterboxForm").submit();
				}, { parentId: categoryNode.data('category'), elementToAdd: elementToAdd[0] }));
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

var expandFilterBox = function() {
	// get menu position to place filterbox
	var position = $("#menu").offset();
	position.top = position.top + $("#menu").outerHeight();

	$("#filterbox").css({left: position.left, top: position.top }).slideToggle();

	// make arrow disappear
	$("#menu #menuArrow").hide();
}

var collapseFilterBox = function() {
	$("#filterbox").slideToggle({
		complete: function() {
			// make arrow reappear
			$("#menu #menuArrow").show();
		}
	});

}