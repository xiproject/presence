var xal = require('../../xal-javascript');
var spawn = require('child_process').spawn;

var presenceCertainty = 0.0;
var present = false;

var decayTime = 6000;

function onPresenceDetected() {
    if (presenceCertainty <= 0) {
        xal.createEvent('xi.event.inform.user.presence', function(state, done) {
            state.put('xi.event.inform.user.presence', true);
            done(state);
        });
    }
    presenceCertainty = 1.0;
    present = true;
}

function decayCertainty() {
    if (presenceCertainty > 0) {
        presenceCertainty -= 0.1;
    }
    else {
        xal.log.info('Absence detected');
        if (!present) {
            return;
        }
        presenceCertainty = 0;
        present = false;
        xal.createEvent('xi.event.inform.user.presence', function(state, done) {
            state.put('xi.event.inform.user.presence', false);
            done(state);
        });
    }
}

setInterval(decayCertainty, decayTime);

xal.on('xi.event.ask.user.presence', function(state, next) {
    state.put('xi.event.inform.user.presence', {
        value: presenceCertainty > 0,
        certainty: presenceCertainty
    });
    next(state);
});

xal.on('xi.event.input', function(state, next) {
    xal.log.debug('Presence detected: input event');
    onPresenceDetected();
});


var presence = spawn('./presence.py', [], {
    cwd: process.cwd(),
    env: process.env
});

presence.stdout.setEncoding('utf8');
presence.stderr.setEncoding('utf8');

presence.stdout.on('data', function(data) {
    if (data.match(/Presence detected/)) {
        xal.log.debug(data);
        onPresenceDetected();
    }
});

presence.stderr.on('data', function(data) {
    xal.log.warn('stderr: ', data);
});

presence.on('close', function(code, signal) {
    xal.log.fatal('presence.py closed');
});

xal.start({name: 'Presence'});
