$(function() {
	$('#filterbox [id$="_Toggle"]').click(function() {
		var tokens = $(this).attr("id").split("_");
		tokens.pop();
		var toggleTarget = tokens.join("_");

		var position = $("#filterbox").offset();

		position.top = position.top + $("#filterbox").outerHeight();


		$("#"+toggleTarget).css({left: position.left, top: position.top }).slideToggle();
	});

	$("#filterbox #id_date").datepicker({
		onSelect: function() {
			APP.filtersChanged = true;
		},
		changeYear: true,
		changeMonth: true
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

var buildFilterBox = function(treedata, checked_nodes, special, specific_feeling, chosen_date) {
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

					// if whole row is selected, select category as well
					// WARNING: MESSES UP NEXT CHECK, MUST BE FIRST
					if($(this.elementToAdd).siblings(":not(.catName)").not('.active').length == 0) {
						this.parent.addClass('active');
					}

					// if category selected, and I was just deselected, deselect category
					if( !$(this.elementToAdd).hasClass('active') && this.parent.hasClass('active') ) {
						this.parent.removeClass('active');
					}

					APP.filtersChanged = true;
				}, { parent: categoryNode, elementToAdd: elementToAdd }));
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

  if(filtersEmpty(checked_nodes, special, specific_feeling, chosen_date)) {
    expandFilterBox();
  }
};

var filtersEmpty = function(checked_nodes, special, specific_feeling, chosen_date) {
  if (typeof(checked_nodes) !== "undefined" && checked_nodes.length > 0) {
    return false;
  }

  if (typeof(special) !== "undefined") {
    if (special.blackwhite || typeof(special.intensities) !== "undefined" && special.intensities.length > 0) {
      return false;
    }
  }

  if (specific_feeling !== null) {
    return false;
  }

  if (chosen_date !== null) {
    return false;
  }

  return true;
};

var expandFilterBox = function() {
	// get menu position to place filterbox
	var position = $("#menu").offset();
	position.top = position.top + $("#menu").outerHeight();

	$("#filterbox").css({left: position.left, top: position.top }).slideToggle();

	// make arrow disappear
	$("#menu #menuArrow").hide();
};

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

};
