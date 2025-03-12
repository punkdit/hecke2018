#!/usr/bin/env python


from time import sleep, time
start_time = time()
from random import choice, random, randint
from functools import reduce
from functools import reduce, lru_cache
cache = lru_cache(maxsize=None)
from operator import add, mul
from math import prod


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

def render(p, l, F, gen):
    N = p**l - 1
    assert N==len(gen)
    R = N/8
    r = 0.3
    cvs = Canvas()
    
    cvs.text(0, R+1.0, "GF(%d)"%(p**l), [Scale(2)]+st_south)
    cvs.stroke(path.circle(0,0,1.3*R), [white])
    
    pts = []
    for i in range(N):
        theta = 2*pi*i/N
        x = R*sin(theta)
        y = R*cos(theta)
        pts.append((x,y))
    
        #cvs.fill(path.circle(x, y, 0.1), [blue])
        #m = 1.05
        #cvs.text(m*x, m*y, r"$x^{%d}$"%i, st_center)

    for i in range(N):
        j = (i*p)%N
        #cvs.stroke(path.line(*pts[i], *pts[j]), [blue.alpha(0.5)] + st_THIck)
        assert F.cycle[i]**p == F.cycle[(i*p)%N]

    remain = set(range(N))
    orbits = []
    while remain:
        i = remain.pop()
        orbit = [i]
        while 1:
            j = (orbit[-1]*p)%N
            if j==orbit[0]:
                break
            orbit.append(j)
            remain.remove(j)
        orbits.append(orbit)

    cls = {2:black, 3:red, 6:blue}
    orbits.sort(key = len, reverse=True)
    for orbit in orbits:
        K = len(orbit)
        if K==1:
            continue
        cl = cls[K]
        for idx in range(K):
            i,j = orbit[idx], orbit[(idx+1)%K]
            cvs.stroke(
                path.line(*pts[i], *pts[j]), [cl.alpha(0.7)] + st_THIck)
            i = j
        print(len(orbit), end=" ")
    print()
        
    def make(x, y, a):
        pth = path.circle(x, y, r)
        cvs.fill(pth, [white])
        cvs.stroke(pth, [black])

        rr = 0.6*r
        for j in range(l):
            theta = 2*pi*j/l
            x1 = x + rr*sin(theta)
            y1 = y + rr*cos(theta)
            pth = path.circle(x1, y1, r/4)
            if a[j]==1:
                cvs.fill(pth)
            cvs.stroke(pth)
        
    for i in range(N):
        x, y = pts[i]
        make(*pts[i], gen[i])

    make(0, 0, F.promote(0))

    return cvs

        
# ------------------------------------------------------

from bruhat.slow_element import PolynomialRing, FiniteField, GaloisField
from bruhat.util import cross
from bruhat.gset import Perm, mulclose, Group
from bruhat import elim

def GF(p, l):
    Fp = FiniteField(p)
    ring = PolynomialRing(Fp)
    x = ring.x
    for coeffs in cross([list(range(p))]*l):
        op = "+".join("%d*x**%d"%(v,i) for (i,v) in enumerate(coeffs))
        op = "lambda x : (%s+x**%d)"%(op,l)
        fn = eval(op)
        vals = [fn(x)%p for x in range(p)]
        if 0 in vals:
            continue
        F = GaloisField(ring, fn(x))
        #yield coeffs, fn
        roots = []
        for a in F.elements:
            if fn(a)==0:
                roots.append(a)
        if len(roots) != l:
            continue
        F.roots = roots
        F.coeffs = coeffs
        F.fn = fn
        F.op = op
        yield F

#def dot(B, v):
#    l = len(B)
#    u = []
#    for i in range(l):
#        r = reduce(add, [B[i,j]*v[j] for j in range(l)])
#        u.append(r)
#    return u


#for p in [2, 3, 5, 7, 11]:
for p in [2,3,5,7]:
  for l in [2,3,4,5]:

    if p**l > 5**3:
        continue

for (p,l) in [(2,6)]:

    print()
    print("GF(%d^%d)"%(p,l))
    count = 0
    for F in GF(p,l):
        if F.coeffs[-1] != p-1:
            continue
        #print(F)
        els = set(F.elements)
        #for a in F.elements:
        #    for b in F.elements:
        #        assert a+b in els
        #        assert a*b in els

        # we'd like x to be a generator
        a = F.x
        cycle = []
        b = F.promote(1)
        for i in range(1, p**l):
            cycle.append(b)
            b = a*b
            if b == 1:
                break
        else:
            assert 0
        if i != p**l - 1:
            continue # <--------- not a generator
        assert len(cycle) == p**l-1
        F.cycle = cycle

        frob = lambda x : x**p

        # re-order the roots
        #roots = F.roots
        roots = [F.x]
        for i in range(l-1):
            roots.append( frob(roots[-1]) )
        for a in roots:
            assert frob(a) in roots
            assert F.fn(a) == 0
        rows = []
        for a in roots:
            rows.append([a[i] for i in range(l)])
        A = elim.array(rows)
        if elim.rank(F, A) != l:
            continue # wtf.
        print(F.coeffs, F.op)
        for a in roots:
            print("\t", a)
        #print(elim.shortstr(A))
        B = elim.pseudo_inverse(F, A, check=True)
        #print(elim.shortstr(B))
        AB = elim.dot(F, A, B)
        #print(elim.shortstr(AB))
        assert reduce(add, roots) == -F.coeffs[-1]
        assert reduce(mul, roots) == ((-1)**l) * F.coeffs[0]

        gen = []
        for a in cycle:
            v = elim.array([a[i] for i in range(l)]).reshape((l,))
            u = elim.dot(F, v, B)
            gen.append(u)
        assert cycle[0]==1

        cvs = render(p, l, F, gen)
        save("neck_%d_%d_%d"%(p,l,count))
        count += 1
        #break

exit()

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
    
    #save("cusp_%d"%p)

    
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


    






