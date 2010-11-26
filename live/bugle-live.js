var Faye = require('./lib/faye-node');
var fs = require('fs');
var sys = require('sys');

var settings = JSON.parse(fs.readFileSync(process.argv[2] || './settings.json').toString());

var debug = function (s) {
    if (settings.debug) {
        sys.debug(s);
    }
};

var fayeServer = new Faye.NodeAdapter({
    mount:    '/faye',
    timeout:  45
});

debug("Starting Faye server on port "+settings.port);
fayeServer.listen(settings.port);

