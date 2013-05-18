function loadTree(treedata, checked_nodes) {
	// initially load the whole first level
	var initially_load = [];
	for(var i = 0; i < treedata.length; i++) {
		var node = treedata[i];
		initially_load.push(node.attr.id);
	}

	var tree = $('#feelingtree').bind("loaded.jstree", function (event, data) {
		if(typeof(checked_nodes) === "undefined" || checked_nodes.length == 0) {
			expandFilterBox();
		}
		/*for(var node in checked_nodes) {
		 initially_load.push("#virtue_node");
		 //initially_load.push("#"+checked_nodes[node]+"_node");
		 }*/
		for(var i = 0; i < checked_nodes.length; i++) {
			data.inst.check_node("#"+checked_nodes[i]+"_node");
		}
	})
	.jstree({
		'core': {
			'html_titles': true,
			'initially_load': initially_load
		},
		'json_data': {
			'data': treedata
		},
		'themes': {
			'icons': false
		},
		'checkbox': {
			'override_ui': false,
			'real_checkboxes': true,
			'real_checkboxes_names': function(n) {
				var feeling = $.trim(n.children("a").text());

				if(feeling == "")
				{ /* this is a second level node */
					feeling = $.trim(n.parent().closest("li").children("a").text())+"_"+n.index();
				}
				
				return [feeling+"_check", 'feeling', feeling];
			}
		},
		'search': {
			'show_only_matches': true
		},
		plugins: ['themes', 'json_data', 'ui', 'checkbox', 'search']
	});
	return tree;
}
