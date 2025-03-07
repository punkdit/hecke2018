#!/usr/bin/env python


from time import sleep, time
start_time = time()
from random import choice, random, randint

import numpy
from numpy import array

#from bruhat.action import Group, Perm, mulclose_fast

from huygens import config
config(text="pdflatex")
from huygens.back import arc_to_bezier
from huygens.front import *
from huygens.pov import *
from huygens.namespace import *
from huygens.loadsvg import loadsvg

# ------------------------------------------------------
# trigger rebuild
import atexit
import pathlib
def fini():
    pathlib.Path('build').touch()
    print("took %.3f seconds"%(time() - start_time))
    print()

atexit.register(fini)
# ------------------------------------------------------


def save(name):
    print("save(%r)"%(name,))
    cvs.writePDFfile("images/"+name+".pdf")
    cvs.writeSVGfile("images/"+name+".svg")


# ------------------------------------------------------


N = 24

R = 10.0
cvs = Canvas()

cvs.stroke(path.circle(0,0,1.3*R), [white])

pts = []
for i in range(N):

    theta = 2*pi*i/N
    x = R*sin(theta)
    y = R*cos(theta)
    pts.append((x,y))

    cvs.fill(path.circle(x, y, 0.1), [blue])
    m = 1.05
    cvs.text(m*x, m*y, r"$x^{%d}$"%i, st_center)

for i in range(N):
    j = (i*5)%N
    if j <= i:
        continue
    cvs.stroke(path.line(*pts[i], *pts[j]), [blue.alpha(0.5)] + st_THIck)


save("cusp_24")


    






