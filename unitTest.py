#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
from processJson import processJson

input_json_filename = 'request.json'
ouput_json_filename = 'response.json'
conf_thres = 0.05


with open(input_json_filename, 'r') as input_json_file:
    json_str = input_json_file.read().replace('\n', '')
    
    ouput_json_filename
    
request = json.loads(json_str)

response = processJson(request, conf_thres)

print response
print 'save the output in file "response.json" ...'

ouput_json_file = open(ouput_json_filename, "w")
ouput_json_file.write(response)
ouput_json_file.close()

print "done!"