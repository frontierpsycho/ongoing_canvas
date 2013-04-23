/* depends: init.js, interaction.js */

var addShape = function(data) {
	var remove_list = string_to_list(data["remove"]);
	remove_list.forEach(function(item) {
		APP.shapes[item].remove();
	});

	APP.shapes[data["fd_id"]] = paper.path(data["shape"]).attr({ fill: data["colour"], "stroke" : "none" }).transform(Raphael.matrix(data['transform'][0], data['transform'][1], data['transform'][2], data['transform'][3], data['transform'][4], data['transform'][5]).toTransformString());

	add_interaction(APP.shapes[data["fd_id"]], data["fd_id"], data["colour"]);
};

var socket = new io.Socket();
socket.connect();
socket.on('connect', function() {
	socket.subscribe('shapes');
	socket.on("message", addShape);
});

function string_to_list(str)
{
	if(str == "None")
	{
		l = new Array();
	} else {
		str = str.substring(1, str.length-1);
		l = str.split(",");
	}
	return l;
}
