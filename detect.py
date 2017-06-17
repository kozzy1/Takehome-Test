#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from caffe2.proto import caffe2_pb2
import numpy as np
import skimage.io
import skimage.transform
from matplotlib import pyplot
import os
from caffe2.python import core, workspace
import urllib2

def crop_center(img,cropx,cropy):
    y,x,c = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)    
    return img[starty:starty+cropy,startx:startx+cropx]

def rescale(img, input_height, input_width):
    aspect = img.shape[1]/float(img.shape[0])
    if(aspect>1):
        # landscape orientation - wide image
        res = int(aspect * input_height)
        imgScaled = skimage.transform.resize(img, (input_width, res))
    if(aspect<1):
        # portrait orientation - tall image
        res = int(input_width/aspect)
        imgScaled = skimage.transform.resize(img, (res, input_height))
    if(aspect == 1):
        imgScaled = skimage.transform.resize(img, (input_width, input_height))
    return imgScaled


def detect(net, img_url, classlist, conf_thres):

    # rescale image 
    INPUT_IMAGE_SIZE = 227
    img = skimage.img_as_float(skimage.io.imread(img_url)).astype(np.float32)
    img = rescale(img, INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE)
    img = crop_center(img, INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE)

	# transform into CHW order
    img = img.swapaxes(1, 2).swapaxes(0, 1)

	# transform into BGR order
    img = img[(2, 1, 0), :, :]

	# substract mean
    mean = 128
    img = img * 255 - mean
    img = img[np.newaxis, :, :, :].astype(np.float32)

    results = net.run([img])
    results = np.asarray(results)
    results = np.delete(results, 1)
    
    arr = np.empty((0,2), dtype=object)
    arr[:,0] = int(10)
    arr[:,1:] = float(10)
    for i, r in enumerate(results):
        i=i+1
        arr = np.append(arr, np.array([[i,r]]), axis=0)
        
            
    arr = sorted(arr, key=lambda x: x[1], reverse=True)
    output = []
    for ele in arr:
        if ele[1] >= conf_thres:
            output_ele = {}
            output_ele["class"] = classlist[int(ele[0])]
            output_ele["confidence"] = ele[1]
            output.append(output_ele)
        
    return output




