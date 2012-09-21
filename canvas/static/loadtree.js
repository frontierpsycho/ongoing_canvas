function loadTree(treedata, checked_nodes) {
	var tree = $('#feelingtree').jstree({
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
			console.log(checked_nodes[node]);
			data.inst.check_node("#"+checked_nodes[node]+"_check");
		}
	});
	return tree;
}
