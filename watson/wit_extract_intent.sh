#!/bin/sh

read transcription
queryparam=$(echo $transcription | sed 's/ /%20/g')

curl -XGET "https://api.wit.ai/message?v=20141022&q=$queryparam" -H "Authorization: Bearer GSPHSOOVWHDRON4S6QM7PRN3TZM253XM"
