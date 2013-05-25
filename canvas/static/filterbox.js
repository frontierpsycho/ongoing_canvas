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

var buildFilterBox = function(treedata, checked_nodes, special) {
	var tree = $.jstree._reference("#feelingtree");

	for(var i = 0; i < treedata.length; i++) {
		var treeNode = treedata[i];
		var category = treeNode.data.charAt(0).toUpperCase() + treeNode.data.substring(1);
		var categoryNode = $("td.catName:contains('"+category+"')");
		categoryNode.data('category', "#"+treeNode.attr.id);
		var categoryActive = false;
		if($.inArray(treeNode.attr.id.replace(/_node$/, ""), checked_nodes) > -1) {
			categoryNode.addClass("active");
			categoryActive = true;
		}

		if(treeNode.hasOwnProperty('children')) {
			for(var j = treeNode.children.length-1; j >= 0 ; j--) {
				var child = treeNode.children[j];
				var checkboxId = "#"+child.attr.id;
				var elementToAdd = $.parseHTML('<td data-category="'+checkboxId+'">'+child.data+'</td>')[0];
				if(categoryActive || $.inArray(child.attr.id.replace(/_node$/, ""), checked_nodes) > -1) {
					$(elementToAdd).addClass("active");
				}

				categoryNode.after(elementToAdd);
				$(elementToAdd).click($.proxy(function(event) {
					var nodeId = $(this.elementToAdd).data('category');
					//tree.load_node(this.parentId, function() {}, function() {});
					if(tree.is_checked(nodeId)) {
						tree.uncheck_node(nodeId);
					} else {
						tree.check_node(nodeId);
					}
					$(this.elementToAdd).toggleClass('active');
					APP.filtersChanged = true;
				}, { parentId: categoryNode.data('category'), elementToAdd: elementToAdd }));
			}
		}

		categoryNode.click($.proxy(function(event) {
			var nodeId = "#"+this.category+"_node";
			if(tree.is_checked(nodeId)) {
				tree.uncheck_node(nodeId);
			} else {
				tree.check_node(nodeId);
			}
			this.node.toggleClass('active');
			if(this.node.hasClass('active')) {
				this.node.siblings().addClass('active');
			} else {
				this.node.siblings().removeClass('active');
			}
			APP.filtersChanged = true;
		}, { node: categoryNode, category: category }));
	}

	var specialNames = ['blackwhite', 'intensity0', 'intensity1','intensity2', 'intensity3']
	var activateSpecial = function(name) {
		return function() {
			$(this).parent('td').toggleClass('active');
			$("#filterboxForm #id_"+name).val($(this).parent('td').hasClass('active'));
			APP.filtersChanged = true;
		};
	};
	for(var i = 0; i < specialNames.length; i++) {
		if(specialNames[i].indexOf('intensity') == 0) {
			// this is an intensity, if activated add class
			intensity = parseInt(specialNames[i].charAt(specialNames[i].length - 1));
			if(special.intensities.indexOf(intensity) != -1) {
				$("#"+specialNames[i]).parent('td').addClass('active');
			}
		} else {
			// this is blackwhite, if activated add class
			if(special.blackwhite) {
				$("#"+specialNames[i]).parent('td').addClass('active');
			}
		}
		$("#"+specialNames[i]).click(activateSpecial(specialNames[i]));
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
			if(APP.filtersChanged) {
				$("#filterboxForm").submit();
			}
		}
	});

}