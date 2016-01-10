#!/usr/bin/python
import sys
import json

def extract_transcript(result):
	alternatives = result['alternatives']
	if len(alternatives) == 0:
		return None
	else:
		return alternatives[0]["transcript"]

def parse_watson_response(json_response):
        parsed_json = json.loads(json_response)
        results = parsed_json['results']
        if len(results) == 0:
        	exit()
        result = results[0]
	
	transcript = None

        if 'alternatives' in result:
        	transcript = extract_transcript(result)

        print transcript

if __name__ == "__main__":
        for line in sys.stdin:
                parse_watson_response(line)
