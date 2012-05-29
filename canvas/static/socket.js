var addShape = function(shape) {
	alert(shape);
};

var socket = new io.Socket();
socket.connect();
socket.on('connect', function() {
	socket.subscribe('shapes');
	socket.on("message", addShape);
});

