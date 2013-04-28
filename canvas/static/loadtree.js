function loadTree(treedata, checked_nodes) {
	var tree = $('#feelingtree').jstree({
		'core': {
			'html_titles': true
		},
		'json_data': {
			'data': treedata,
			'progressive_render': true

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
	}).bind("loaded.jstree", function (event, data) { 
		for(node in checked_nodes)
		{
			data.inst.check_node("#"+checked_nodes[node]+"_check");
		}
	});
	return tree;
}
