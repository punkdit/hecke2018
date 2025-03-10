#!/usr/bin/env python


from time import sleep, time
start_time = time()
from random import choice, random, randint

import numpy
from numpy import array

#from bruhat.action import Group, Perm, mulclose_fast

from huygens import config
config(text="pdflatex",
latex_header=r"""
\usepackage[vcentermath]{genyoungtabtikz}
\Yboxdim{8pt}
"""
)
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


for p in [2, 3, 5, 7, 11]:
    N = p**2 - 1
    R = 1.6*p
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
        j = (i*p)%N
        #if j <= i:
        #    continue
        cvs.stroke(path.line(*pts[i], *pts[j]), [blue.alpha(0.5)] + st_THIck)
    
    save("cusp_%d"%p)

    
# ------------------------------------------------------

for l in [2,3,4,6]:
    for p in [2, 3, 5]:
        N = p**l - 1
        R = N/8
        cvs = Canvas()
        
        cvs.stroke(path.circle(0,0,1.3*R), [white])
        
        pts = []
        for i in range(N):
            theta = 2*pi*i/N
            x = R*sin(theta)
            y = R*cos(theta)
            pts.append((x,y))
        
            cvs.fill(path.circle(x, y, 0.1), [blue])
            #m = 1.05
            #cvs.text(m*x, m*y, r"$x^{%d}$"%i, st_center)
        
        for i in range(N):
            j = (i*p)%N
            cvs.stroke(path.line(*pts[i], *pts[j]), [blue.alpha(0.5)] + st_THIck)
        
        save("cusp_%d_%d"%(p,l))
    
    
exit()



# ------------------------------------------------------

reps = r"""
\yng(2)(A)\bigoplus \yng(1,1)(C)\bigoplus B\otimes D\bigoplus H\bigoplus J
A\otimes B\bigoplus C\otimes D\bigoplus E\bigoplus K
\yng(1,1)(B)\bigoplus \yng(1,1)(D)\bigoplus A\otimes C\bigoplus F
A\otimes D\bigoplus B\otimes C\bigoplus G\bigoplus I
\yng(1,1)(A)\bigoplus \yng(1,1)(C)\bigoplus B\otimes D\bigoplus H
A\otimes B\bigoplus C\otimes D\bigoplus E\bigoplus K
\yng(2)(B)\bigoplus \yng(1,1)(D)\bigoplus A\otimes C\bigoplus F\bigoplus M
A\otimes D\bigoplus B\otimes C\bigoplus I\bigoplus N
\yng(1,1)(A)\bigoplus \yng(1,1)(C)\bigoplus B\otimes D\bigoplus J
A\otimes B\bigoplus C\otimes D\bigoplus K\bigoplus L
\yng(1,1)(B)\bigoplus \yng(1,1)(D)\bigoplus A\otimes C\bigoplus F
A\otimes D\bigoplus B\otimes C\bigoplus I\bigoplus N
\yng(1,1)(A)\bigoplus \yng(2)(C)\bigoplus B\otimes D\bigoplus H\bigoplus J
A\otimes B\bigoplus C\otimes D\bigoplus E\bigoplus L
\yng(1,1)(B)\bigoplus \yng(1,1)(D)\bigoplus A\otimes C\bigoplus M
A\otimes D\bigoplus B\otimes C\bigoplus G\bigoplus I
\yng(1,1)(A)\bigoplus \yng(1,1)(C)\bigoplus B\otimes D\bigoplus J
A\otimes B\bigoplus C\otimes D\bigoplus E\bigoplus L
\yng(1,1)(B)\bigoplus \yng(2)(D)\bigoplus A\otimes C\bigoplus F\bigoplus M
A\otimes D\bigoplus B\otimes C\bigoplus G\bigoplus N
\yng(1,1)(A)\bigoplus \yng(1,1)(C)\bigoplus B\otimes D\bigoplus H
A\otimes B\bigoplus C\otimes D\bigoplus K\bigoplus L
\yng(1,1)(B)\bigoplus \yng(1,1)(D)\bigoplus A\otimes C\bigoplus M
A\otimes D\bigoplus B\otimes C\bigoplus G\bigoplus N
""".strip().split("\n")
assert len(reps) == 24, len(reps)

N = 24

R = 8.0
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

    deco = reps[i]
    m = 1.15
    cvs.text(m*x, m*y, "$%s$"%deco, [Rotate(theta-pi/6)])


for i in range(N):
    j = (i*5)%N
    if j <= i:
        continue
    cvs.stroke(path.line(*pts[i], *pts[j]), [blue.alpha(0.5)] + st_THIck)


save("cusp_24")


    






