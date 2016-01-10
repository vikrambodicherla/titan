#!/bin/sh
curl -u eac53bf1-3a57-4961-883d-2358faca7354:AHLfzHrA6QUw -X POST --header "Content-Type: audio/flac" --header "Transfer-Encoding: chunked" --data-binary @$1 "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?keywords=move&keywords_threshold=0.25"
