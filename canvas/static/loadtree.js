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
		plugins: ['themes', 'json_data', 'ui', 'checkbox']
	}).bind("loaded.jstree", function (event, data) { 
		console.log(checked_nodes.length);
		for(node in checked_nodes)
		{
			console.log(checked_nodes[node]);
			data.inst.check_node("#"+checked_nodes[node]+"_node");
		}
	});
	return tree;
}
