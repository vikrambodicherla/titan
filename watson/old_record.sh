#!/bin/sh
arecord -d 2 -D plughw:1,0 -q -f cd -t wav -d 0 -r 48000 | flac - -f --best --sample-rate 48000 -s -o $1;
