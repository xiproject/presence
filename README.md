# Presence

The presence agent for [Zeus](http://xiproject.github.io/zeus). This detects user presence by listening for sound and doing motion detection and face detection.

## Prerequisites

- node v0.10
- [bunyan](https://github.com/trentm/node-bunyan) for pretty printing logs.
- Python 2 installed and on your path

## Installation

Clone the repo, `cd` into it and run `npm install`.

## Run

```sh
$ node index.js --logfile presence.log 2>&1 | bunyan
```

## Caveats

- `presence` uses the Open CV library to do motion detection and face detection from your webcam's stream. This is quite CPU intensive at the moment.
- `presence` also listens on the microphone stream for sound above a certain threshold. This may cause issues with other applications trying to use your mic.
