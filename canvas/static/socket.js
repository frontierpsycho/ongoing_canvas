var addShape = function(shape) {
	paper.path(shape["shape"]).attr({ fill: shape["colour"], "stroke" : "none" }).transform(Raphael.matrix(shape['transform'][0], shape['transform'][1], shape['transform'][2], shape['transform'][3], shape['transform'][4], shape['transform'][5]).toTransformString());
};

var socket = new io.Socket();
socket.connect();
socket.on('connect', function() {
	socket.subscribe('shapes');
	socket.on("message", addShape);
});

