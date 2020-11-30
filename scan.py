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
    #print('SANE version:', ver)
    
    devices = sane.get_devices()
    #print('Available devices:', devices)
    
    dev = sane.open(devices[0][0])
    
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
    
    #params = dev.get_parameters()
    #print('params:', params)
    
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

    dev.start()
    im = dev.snap()
    w, h = im.size
    r = 2.
    im = im.resize((int(w/r), int(h/r)))
    im.save(name)
    dev.close()
    print("saved", name)
    

if __name__ == "__main__":

    name = argv.next()
    main(name)

    
