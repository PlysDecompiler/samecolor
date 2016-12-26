"""
This module contains collision test functions.
Note:
The naming convention used is lowerdimensional and less complex objects are named first.
""" 
from __future__ import division

import itertools
import math

#def point_point(x1,y1,x2,y2,dist = 0.001):  # this kind of is circle circle 
#    return math.pow(x1-x2,2) + math.pow(y1-y2,2) < math.pow(dist, 2)     # if within circle


def point_point(p1, p2, dist = 0.001):  # this kind of is circle circle 
    return math.pow(p1[0]-p2[0], 2) + math.pow(p1[1]-p2[1], 2) < math.pow(dist, 2)     # if within circle

def point_point_alt(p1, p2, vec):
    return math.pow(p1[0]-p2[0], 2) + math.pow(p1[1]-p2[1], 2) <= math.pow(vec[0], 2) + math.pow(vec[1], 2)


    
#how to determine the direction in which the point may/not pass the line
#the line has to be given in mathematical positive direction, outside is on the right side    
def point_line(px1,py1,lx1,ly1,lx2,ly2):
    pass


def line_line(l1x1,l1y1,l1x2,l1y2,l2x1,l2y1,l2x2,l2y2, already_used=0):
    if l2x2==l2x1: 
        if already_used:
            return False 
        else:
            return line_line(l1y1,l1x1,l1y2,l1x2,l2y1,l2x1,l2y2,l2x2, 1)
    
    n =  float( ((l1y2-l1y1)*(l2x2-l2x1)-(l1x2-l1x1)*(l2y2-l2y1)))
    if (n==0): return False
    
    r = float( ( (l1x1-l2x1)*(l2y2-l2y1)+(l2y1-l1y1)*(l2x2-l2x1) )/n)
    s = float(( l1x1 - l2x1 + r*(l1x2-l1x1) )/(l2x2-l2x1))
    
    return (r>=0 and r<=1 and s>=0 and s<=1)

    
def point_square(x1,y1,x2,y2,dist = 0.001):  # second point is center of square 
    return abs(x2-x1) <= dist and abs(y2-y1) <= dist

def triangle_sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])


#to test if rectangles intersect, to test which points are not eligable for positioning polygons
def point_in_triangle(pt, v1, v2, v3):
    b1 = triangle_sign(pt, v1, v2) < 0.
    b2 = triangle_sign(pt, v2, v3) < 0.
    b3 = triangle_sign(pt, v3, v1) < 0.
    return ((b1 == b2) and (b2 == b3))


def point_in_triangle_on_line(pt, v1, v2, v3):
    b1 = triangle_sign(pt, v1, v2) <= 0.
    b2 = triangle_sign(pt, v2, v3) <= 0.
    b3 = triangle_sign(pt, v3, v1) <= 0.
    return ((b1 == b2) and (b2 == b3))



def line_line_intersection(l1x1,l1y1,l1x2,l1y2,l2x1,l2y1,l2x2,l2y2):
    x = ((l1x1*l1y2-l1y1*l1x2)*(l2x1-l2x2)-(l1x1-l1x2)*(l2x1*l2y2-l2y1*l2x2))/ \
        ((l1x1-l1x2)*(l2y1-l2y2)-(l1y1-l1y2)*(l2x1-l2x2))
    
    y = ((l1x1*l1y2-l1y1*l1x2)*(l2y1-l2y2)-(l1y1-l1y2)*(l2x1*l2y2-l2y1*l2x2))/ \
        ((l1x1-l1x2)*(l2y1-l2y2)-(l1y1-l1y2)*(l2x1-l2x2))
    return (x,y)


# first two args is point, 3rd and 4th arg is middle of plgrm, rest is side-vectors
def point_in_parallelogram(px, py, mx, my, v1x, v1y, v2x, v2y):
    A = (mx-v1x-v2x,my-v1y-v2y)
    B = (mx+v1x-v2x,my+v1y-v2y)
    C = (mx+v1x+v2x,my+v1y+v2y)
    D = (mx-v1x+v2x,my-v1y+v2y)
    
    if point_in_triangle_on_line((px,py), A, B, C) or point_in_triangle_on_line((px,py) , C, D, A):
        return True
    else:
        return False


#put that in a util module
def square_outline(size):
    a = [(i,size) for i in range(-size, size+1)]
    b = [i[::-1] for i in a]
    c = [(i,-size) for i in range(-size, size+1)]
    d = [i[::-1] for i in c]
    return set(a+b+c+d)


def distance(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)


mSize = 700.
gS = 200.
scal = 1.0

def gamepos_to_mousepos(pos, playerpos=(0,0), mS = mSize):
    return  [(pos[0]-playerpos[0])*mS/gS + mS/2
                  ,(pos[1]-playerpos[1])*(-mS/gS) + mS/2
                  ]

def mousepos_to_gamepos(pos, playerpos=(0,0), mS = mSize):
    return  [scal*(playerpos[0]+(pos[0]-mS/2)/(mS/gS)),
                         scal*(playerpos[1]-(pos[1]-mS/2)/(mS/gS))]

