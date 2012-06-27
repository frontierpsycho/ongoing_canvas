var page = require('webpage').create(), address;
page.onConsoleMessage = function (msg) {
		    console.log(msg);
};

if (phantom.args.length === 0) {
		console.log('Usage: get_snapshot.js <some URL>');
		phantom.exit();
} else {
		address = phantom.args[0];
		page.open(address, function (status) {
				if (status !== 'success') {
						console.log('FAIL to load the address');
				} else {
					var results = page.evaluate(function() {
							var svg = document.getElementsByTagName("svg")[0];
							var doc = document.documentElement.innerHTML;
							console.log(doc.substring(doc.indexOf("<svg"), doc.indexOf("</svg") + 6));
							return svg
					});
				}
				phantom.exit();
		});
}
