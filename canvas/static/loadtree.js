function loadTree(treedata, initially_open) {
	$('#feelingtree').jstree({
		'json_data': {
			'data': treedata
		},
		'themes': {
			'icons': false
		},
		'initially_open': initially_open,
		'checkbox': {
			'override_ui': false,
			'real_checkboxes': true,
			'real_checkboxes_names': function(n) {
				console.log(n.children("a").text());
				
				return ['feeling', $.trim(n.children("a").text())];
			}
		},
		plugins: ['themes', 'json_data', 'ui', 'checkbox']
	});
}
