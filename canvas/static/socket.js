var addShape = function(data) {
	paper.path(data["shape"]).attr({ fill: data["colour"], "stroke" : "none" }).transform(Raphael.matrix(data['transform'][0], data['transform'][1], data['transform'][2], data['transform'][3], data['transform'][4], data['transform'][5]).toTransformString());
};

var socket = new io.Socket();
socket.connect();
socket.on('connect', function() {
	socket.subscribe('shapes');
	socket.on("message", addShape);
});

