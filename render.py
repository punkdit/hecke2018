#!/usr/bin/env python3

"""
Convert transcrypt html5 canvas code into PyX calls
and generate svg files in output directory.
"""

import sys, os
from math import *

import pyx 
from pyx import path, deco, trafo, style, text, color, deformer
from pyx.color import rgb, cmyk
from pyx.color import rgbfromhexstring as rgbhex


text.set(mode="latex") 
#text.set(docopt="12pt") # broken
text.preamble(r"\usepackage{amsmath,amsfonts,amssymb}")


black = rgb(0., 0., 0.) 
blue = rgb(0., 0., 0.8)
lred = rgb(1., 0.4, 0.4)
white = rgb(1., 1., 1.) 

#shade = rgb(0.75, 0.55, 0)

grey = rgb(0.75, 0.75, 0.75)
shade = grey
shade0 = rgb(0.75, 0.75, 0.75)
shade1 = rgb(0.80, 0.80, 0.80)
shade2 = rgb(0.85, 0.85, 0.85)

light_shade = rgb(0.85, 0.65, 0.1)
light_shade = rgb(0.9, 0.75, 0.4)


north = [text.halign.boxcenter, text.valign.top]
northeast = [text.halign.boxright, text.valign.top]
northwest = [text.halign.boxleft, text.valign.top]
south = [text.halign.boxcenter, text.valign.bottom]
southeast = [text.halign.boxright, text.valign.bottom]
southwest = [text.halign.boxleft, text.valign.bottom]
east = [text.halign.boxright, text.valign.middle]
west = [text.halign.boxleft, text.valign.middle]
center = [text.halign.boxcenter, text.valign.middle]


st_dashed = [style.linestyle.dashed]
st_dotted = [style.linestyle.dotted]
st_round = [style.linecap.round]
#st_mitre = [style.linecap.square]

st_thick = [style.linewidth.thick]
st_Thick = [style.linewidth.Thick]
st_THick = [style.linewidth.THick]
st_THIck = [style.linewidth.THIck]
st_THICk = [style.linewidth.THICk]
st_THICK = [style.linewidth.THICK]


# -----------------------------------------------------------------------------

c = pyx.canvas.canvas()


W = 2.
H = 2.
r = 0.2
dx = 0.4

x, y = 0., 0.

c.text(x, y, "structure", north)
c.stroke(path.line(x-dx, y+r, x, y+H))
c.stroke(path.line(x+dx, y+r, x, y+H))
c.stroke(path.line(x-dx, y+r, x+dx, y+r))

x += W
c.text(x, y, "symmetry", north)
c.stroke(path.line(x, y+r, x-dx, y+H))
c.stroke(path.line(x, y+r, x+dx, y+H))
c.stroke(path.line(x-dx, y+H, x+dx, y+H))


c.writePDFfile("pic-structure")


# -----------------------------------------------------------------------------


def triangle(x, y, r, deco=[]):

    theta = 0.
    ps = [path.moveto(x + r*sin(theta), y + r*cos(theta))]
    theta += 2*pi/3
    ps.append(path.lineto(x + r*sin(theta), y + r*cos(theta)))
    theta += 2*pi/3
    ps.append(path.lineto(x + r*sin(theta), y + r*cos(theta)))
    ps.append(path.closepath())
    c.stroke(path.path(*ps), deco)


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 1.
triangle(x, y, r, st_THick)

c.writePDFfile("pic-triangle")



# -----------------------------------------------------------------------------


def numbered(x, y, r, nums):

    triangle(x, y, 0.8*r, st_THick)
    theta = 0.
    c.text(x + r*sin(theta), y + r*cos(theta), nums[0], south)
    theta -= 2*pi/3
    c.text(x + r*sin(theta), y + r*cos(theta), nums[1], northeast)
    theta -= 2*pi/3
    c.text(x + r*sin(theta), y + r*cos(theta), nums[2], northwest)


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.7
R = 2.

numbered(x, y, r, "123")
x += R
numbered(x, y, r, "132")
x += R
numbered(x, y, r, "321")
x += R
numbered(x, y, r, "213")
x += R
numbered(x, y, r, "312")
x += R
numbered(x, y, r, "231")
x += R

c.writePDFfile("pic-triangle-numbered")


# -----------------------------------------------------------------------------


def flaged(x, y, r, flags):

    for flag in flags:
        idx = flag[0]
        pos = flag[1]
        if len(flag)==3:
            deco = flag[2]
        else:
            deco = [grey]
        assert idx in [0, 1, 2]
        assert pos in [0, 1]
    
        theta = 2*pi*idx/3
        x0, y0 = (x, y)
        x1, y1 = (x + r*sin(theta), y + r*cos(theta))
        theta += 2.0*pi/6 if pos else -2.0*pi/6
        x2, y2 = (x + 0.5*r*sin(theta), y + 0.5*r*cos(theta))
    
        p = path.path(
            path.moveto(x0, y0),
            path.lineto(x1, y1),
            path.lineto(x2, y2),
            path.closepath())
        #c.stroke(p, deco)
        c.fill(p, deco)

    triangle(x, y, r, st_THick)


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.8
R = 2.

flags = [ (0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0)]
for flag in flags:
    flaged(x, y, r, [flag]); x += R

c.writePDFfile("pic-triangle-frames")


# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.8
R = 2.

for i in range(3):
    st = [(i, 0), (i, 1)]
    flaged(x, y, r, st); x += R

c.writePDFfile("pic-triangle-points")


# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.8
R = 2.


flaged(x, y, r, [(i, 0) for i in range(3)]); x += R
flaged(x, y, r, [(i, 1) for i in range(3)]); x += R

c.writePDFfile("pic-triangle-orientations")


# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = r*2./0.8

tabs = [0., 5*r, 10*r, 10*r+6*R]

def dorow():
    c.stroke(path.rect(tabs[0]-r, y-r, tabs[3]-tabs[0], R))

flags = [ (0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0)]

dorow()
c.text(x, y, "structure", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "subgroup", [pyx.text.size.large])
x = tabs[2]
c.text(x-r, y, "orbit", [pyx.text.size.large])
y -= R; x = tabs[0]
y -= 0.1

dorow()
c.text(x, y, "nothing", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$A$", [pyx.text.size.large])
x = tabs[2]
flaged(x, y, r, flags); x += R
y -= R; x = tabs[0]

dorow()
c.text(x, y, "orientation", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$B$", [pyx.text.size.large])
x = tabs[2]
flaged(x, y, r, [(i, 0) for i in range(3)]); x += R
flaged(x, y, r, [(i, 1) for i in range(3)]); x += R
#c.writePDFfile("pic-triangle-orientations")
y -= R; x = tabs[0]


dorow()
c.text(x, y, "point", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$C$", [pyx.text.size.large])
x = tabs[2]
for i in range(3):
    st = [(i, 0), (i, 1)]
    flaged(x, y, r, st); x += R
#c.writePDFfile("pic-triangle-points")
y -= R; x = tabs[0]


dorow()
c.text(x, y, "frame", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$D$", [pyx.text.size.large])
x = tabs[2]
for flag in flags:
    flaged(x, y, r, [flag]); x += R
#c.writePDFfile("pic-triangle-frames")
y -= R; x = tabs[0]

#c.stroke(path.line(tabs[1], 0, tabs[1], y))

c.writePDFfile("pic-triangle-structures")

# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = r*2./0.8



#         red               green             blue              yellow
colors = [rgbhex("ff1e1e"), rgbhex("3ee53e"), rgbhex("011fff"), rgbhex("fdff57"), ]
def alpha(a):
    return color.transparency(1.0-a)

clr_a = [colors[0], alpha(0.7)]
clr_b = [colors[2], alpha(0.7)]

flags = [ (0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0)]
flags_a = [(i, j, clr_a) for (i, j) in flags]
flags_b = [(i, j, clr_b) for (i, j) in flags]

frames_a = [[flag] for flag in flags_a]
frames_b = [[flag] for flag in flags_b]

points_a = [[(i, 0, clr_a), (i, 1, clr_a)] for i in range(3)]
points_b = [[(i, 0, clr_b), (i, 1, clr_b)] for i in range(3)]

orients_a = [[(i, j, clr_a) for i in range(3)] for j in range(2)]
orients_b = [[(i, j, clr_b) for i in range(3)] for j in range(2)]

nothings_a = [flags_a]
nothings_b = [flags_b]

#for point in points_a:
#    flaged(x, y, r, point); x += R

flaged(x, y, r, nothings_a[0]); x += R
flaged(x, y, r, orients_a[0]); x += R
flaged(x, y, r, points_a[0]); x += R
flaged(x, y, r, frames_a[0]); x += R

y -= R
x = 0.
flaged(x, y, r, nothings_b[0]); x += R
flaged(x, y, r, orients_b[0]); x += R
flaged(x, y, r, points_b[0]); x += R
flaged(x, y, r, frames_b[0]); x += R

c.writePDFfile("pic-triangle-pairs")


# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = r*2./0.8

flaged(x, y, r, points_a[0]); flaged(x, y, r, points_b[1]); x += R
flaged(x, y, r, points_a[0]); flaged(x, y, r, points_b[2]); x += R
flaged(x, y, r, points_a[1]); flaged(x, y, r, points_b[0]); x += R
flaged(x, y, r, points_a[1]); flaged(x, y, r, points_b[2]); x += R
flaged(x, y, r, points_a[2]); flaged(x, y, r, points_b[0]); x += R
flaged(x, y, r, points_a[2]); flaged(x, y, r, points_b[1]); x += R

c.writePDFfile("pic-triangle-point-point-ne")


# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = r*2./0.8

flaged(x, y, r, points_a[0]); flaged(x, y, r, points_b[0]); x += R
flaged(x, y, r, points_a[1]); flaged(x, y, r, points_b[1]); x += R
flaged(x, y, r, points_a[2]); flaged(x, y, r, points_b[2]); x += R


c.writePDFfile("pic-triangle-point-point-eq")


# -----------------------------------------------------------------------------

def do_matrix(x0, y0, r, R, left, right):
    x, y = x0, y0
    for item in left:
        x += R
        flaged(x, y, r, item)
    x, y = x0, y0

    for item in right:
        y -= R
        flaged(x, y, r, item)
    x, y = x0, y0
    for l_item in left:
        x += R
        for r_item in right:
            y -= R
            flaged(x, y, r, l_item)
            flaged(x, y, r, r_item)
        y = y0

    c.stroke(path.rect(x0+0.5*R, y0-0.5*R, R*len(left), -R*len(right)))

    

# -----------------------------------------------------------------------------

c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = 3.*r

do_matrix(x, y, r, R, points_a, points_b)


c.writePDFfile("pic-triangle-point-point-matrix")


# -----------------------------------------------------------------------------

c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = 3.*r

do_matrix(x, y, r, R, points_a, orients_b)


c.writePDFfile("pic-triangle-point-orient-matrix")


# -----------------------------------------------------------------------------

c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = 3.*r

do_matrix(x, y, r, R, orients_a, orients_b)


c.writePDFfile("pic-triangle-orient-orient-matrix")

# -----------------------------------------------------------------------------

c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = 3.*r

do_matrix(x, y, r, R, points_a, nothings_b)


c.writePDFfile("pic-triangle-nothing-point-matrix")


# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = 3.*r

do_matrix(x, y, r, R, frames_a, points_b)


c.writePDFfile("pic-triangle-point-frame-matrix")


# -----------------------------------------------------------------------------

############## SQUARE ########################


def square(x, y, r, deco=[]):

    theta = 2*pi/8.
    ps = [path.moveto(x + r*sin(theta), y + r*cos(theta))]
    theta += 2*pi/4.
    ps.append(path.lineto(x + r*sin(theta), y + r*cos(theta)))
    theta += 2*pi/4.
    ps.append(path.lineto(x + r*sin(theta), y + r*cos(theta)))
    theta += 2*pi/4.
    ps.append(path.lineto(x + r*sin(theta), y + r*cos(theta)))
    ps.append(path.closepath())
    c.stroke(path.path(*ps), deco)


def flaged(x, y, r, flags):

    y += 0.3*r
    for flag in flags:
        idx = flag[0]
        pos = flag[1]
        if len(flag)==3:
            deco = flag[2]
        else:
            deco = [grey]
        assert idx in [0, 1, 2, 3]
        assert pos in [0, 1]
    
        theta = 2*pi*(idx+0.5)/4
        x0, y0 = (x, y)
        x1, y1 = (x + r*sin(theta), y + r*cos(theta))
        theta += 2.0*pi/8 if pos else -2.0*pi/8
        r1 = r/(2**0.5)
        x2, y2 = (x + r1*sin(theta), y + r1*cos(theta))
    
        p = path.path(
            path.moveto(x0, y0),
            path.lineto(x1, y1),
            path.lineto(x2, y2),
            path.closepath())
        #c.stroke(p, deco)
        c.fill(p, deco)

    square(x, y, r, st_THick)


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = r*2.

tabs = [0., 6*r, 11*r, 11*r+8*R/0.8]

def dorow():
    c.stroke(path.rect(tabs[0]-r, y-0.7*r, tabs[3]-tabs[0], R))

flags = [(i, j) for i in range(4) for j in range(2)]

dorow()
c.text(x, y, "structure", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "subgroup", [pyx.text.size.large])
x = tabs[2]
c.text(x-r, y, "orbit", [pyx.text.size.large])
y -= R; x = tabs[0]
y -= 0.1

dorow()
c.text(x, y, "nothing", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$A$", [pyx.text.size.large])
x = tabs[2]
flaged(x, y, r, flags); x += R
y -= R; x = tabs[0]

dorow()
c.text(x, y, "long axis", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$B$", [pyx.text.size.large])
x = tabs[2]
flaged(x, y, r, [(0, 0), (2, 0), (0, 1), (2, 1)]); x += R
flaged(x, y, r, [(1, 0), (3, 0), (1, 1), (3, 1)]); x += R
y -= R; x = tabs[0]

dorow()
c.text(x, y, "short axis", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$C$", [pyx.text.size.large])
x = tabs[2]
flaged(x, y, r, [(0, 0), (2, 0)]); #x += R
flaged(x, y, r, [(1, 1), (3, 1)]); x += R
flaged(x, y, r, [(0, 1), (2, 1)]); #x += R
flaged(x, y, r, [(1, 0), (3, 0)]); x += R
y -= R; x = tabs[0]

dorow()
c.text(x, y, "orientation", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$D$", [pyx.text.size.large])
x = tabs[2]
flaged(x, y, r, [(i, 0) for i in range(4)]); x += R
flaged(x, y, r, [(i, 1) for i in range(4)]); x += R
#c.writePDFfile("pic-triangle-orientations")
y -= R; x = tabs[0]


dorow()
c.text(x, y, "point", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$E$", [pyx.text.size.large])
x = tabs[2]
for i in range(4):
    st = [(i, 0), (i, 1)]
    flaged(x, y, r, st); x += R
y -= R; x = tabs[0]

dorow()
c.text(x, y, "line", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$F$", [pyx.text.size.large])
x = tabs[2]

flaged(x, y, r, [(1-j, j) for j in range(2)]); x += R
flaged(x, y, r, [(2-j, j) for j in range(2)]); x += R
flaged(x, y, r, [(3-j, j) for j in range(2)]); x += R
flaged(x, y, r, [((4-j)%4, j) for j in range(2)]); x += R

y -= R; x = tabs[0]

dorow()
c.text(x, y, "short\&long axis", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$G$", [pyx.text.size.large])
x = tabs[2]
flaged(x, y, r, [(0, 0), (2, 0)]); x += R
flaged(x, y, r, [(0, 1), (2, 1)]); x += R
flaged(x, y, r, [(1, 0), (3, 0)]); x += R
flaged(x, y, r, [(1, 1), (3, 1)]); x += R
y -= R; x = tabs[0]


dorow()
c.text(x, y, "frame", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$H$", [pyx.text.size.large])
x = tabs[2]
for flag in flags:
    flaged(x, y, r, [flag]); x += R
y -= R; x = tabs[0]

#c.stroke(path.line(tabs[1], 0, tabs[1], y))

c.writePDFfile("pic-square-structures")

# -----------------------------------------------------------------------------









