#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import requests
import re

from caffe2.python import workspace
from caffe2.python.models import squeezenet as mynet

from detect import detect

def exists(path):
    try:    
        r = requests.head(path)
    except:
        return False
    return r.status_code == requests.codes.ok

def processJson(request, conf_thres):
    init_net = mynet.init_net
    predict_net = mynet.predict_net
    predict_net.name = "squeezenet_predict"
    workspace.RunNetOnce(init_net)
    workspace.CreateNet(predict_net)
    net = workspace.Predictor(init_net.SerializeToString(), predict_net.SerializeToString())
    
    # object name list
    with open('classnamelist.txt', 'r') as classlistfile:
        classliststr = classlistfile.readlines()
    classlist = [line.partition(":")[2:3][0][2:-3] for line in classliststr]
    
    r_url = re.compile(r"^https?:")
    r_image = re.compile(r".*\.(jpg|png|bmp)$")
    
    img_urls = request["images"]
    
    response = {}
    response["results"] = []
    for img_url in img_urls:
        response_one_img = {}
        response_one_img["url"] = img_url;
        if not r_url.match(img_url):
            response_one_img["error"] = "False URL"
            response["results"].append(response_one_img)
            continue
        if not r_image.match(img_url):
            response_one_img["error"] = "Unsupported Image Format"
            response["results"].append(response_one_img)
            continue
        if not exists(img_url):
            response_one_img["error"] = "Invalid URL"
            response["results"].append(response_one_img)
            continue             

        response_one_img["classes"] = detect(net, img_url, classlist, conf_thres)
        response["results"].append(response_one_img)
         
    response = json.dumps(response, indent=2)
    return response
