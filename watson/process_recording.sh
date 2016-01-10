#!/bin/sh
sh stt.sh $1 | tr -d '\n' | python parse_stt_response.py | ./wit_extract_intent.sh
