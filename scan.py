#!/usr/bin/env python

from __future__ import print_function


# https://python-sane.readthedocs.io/en/latest/

import os, sys

import sane
import numpy
from PIL import Image

from argv import argv


def main(name):

    depth = 8
    mode = 'color'
    
    ver = sane.init()
    print('SANE version:', ver)
    
    devices = sane.get_devices()
    print('Available devices:', devices)
    
    dev = sane.open(devices[1][0])
    
    params = dev.get_parameters()
    #print("params:", params)
    try:
        dev.depth = depth
    except:
        print('Cannot set depth, defaulting to %d' % params[3])
    
    #try:
    #    dev.mode = mode
    #except:
    #    print('Cannot set mode, defaulting to %s' % params[0])
    
    #try:
    #    dev.br_x = 320.
    #    dev.br_y = 240.
    #except:
    #    print('Cannot set scan area, using default')
    
    params = dev.get_parameters()
    print('params:', params)
    
    if name.endswith(".jpg") or name.endswith(".png"):
        pass
    else:
        name += ".jpg"

    try:
        os.stat(name)
        print("%s: file exists!"%name)
        return
    except OSError:
        pass

    #print(dir(dev))
    #return
    for op in dev.get_options():
        print(op)

    dev.mode = "Color"
    dev.resolution = 300
    dev.tl_x = 0.08465576171875#   (0.08465576171875, 215.89999389648438, 0.0))
    dev.tl_y = 0.08465576171875#   (0.08465576171875, 297.0106658935547, 0.0))
    dev.br_x = 215.89999389648438 #   (0.08465576171875, 215.89999389648438, 0.0))
    dev.br_y = 297.0106658935547#   (0.08465576171875, 297.0106658935547, 0.0))

    # (4, 'preview', 'Preview', 'Request a preview-quality scan.', 0, 0, 4, 5, None)
    # (5, 'preview-in-gray', 'Force monochrome preview', 
    # 'Request that all previews are done in monochrome mode.  
    # On a three-pass scanner this cuts down the number of passes to one and on a one-pass scanner, 
    # it reduces the memory requirements and scan-time of the preview.', 0, 0, 4, 5, None)
    # (6, None, 'Geometry', 'Scan area and media size options', 5, 0, 4, 64, None)
    # (7, 'tl-x', 'Top-left x', 'Top-left x position of scan area.', 2, 3, 4, 5, (0.08465576171875, 215.89999389648438, 0.0))
    # (8, 'tl-y', 'Top-left y', 'Top-left y position of scan area.', 2, 3, 4, 5, (0.08465576171875, 297.0106658935547, 0.0))
    # (9, 'br-x', 'Bottom-right x', 'Bottom-right x position of scan area.', 2, 3, 4, 5, (0.08465576171875, 215.89999389648438, 0.0))
    # (10, 'br-y', 'Bottom-right y', 'Bottom-right y position of scan area.', 2, 3, 4, 5, (0.08465576171875, 297.0106658935547, 0.0))

    print("dev.start()")
    dev.start()
    im = dev.snap()
    #im = dev.scan()
    print(im)
    w, h = im.size
    r = 2.
    im = im.resize((int(w/r), int(h/r)))
    im.save(name)
    dev.close()
    print("saved", name)
    

if __name__ == "__main__":

    name = argv.next()
    main(name)

    
