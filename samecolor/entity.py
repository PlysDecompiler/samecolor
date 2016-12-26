# Game: "Samecolor"
# Author: Thomas Strenger
#
#

import math
import random
import itertools
import numpy as np

from samecolor.world import Entity
from samecolor.opengl import *
from samecolor.collision import *


COUNTS = (12,12)
STARTTIERS = 7
EXTREMISM = 0
BIGSIZE = 6
SIZE = 0.95 * BIGSIZE
TILESIZES = np.array([SIZE,SIZE,-SIZE,SIZE,-SIZE,-SIZE,SIZE,-SIZE])
TILESIZES.shape = (4,2)
COLORS = np.array([[255,255,EXTREMISM],[EXTREMISM,255,255],[255,EXTREMISM,255],
                   [255,EXTREMISM,EXTREMISM],[EXTREMISM,EXTREMISM,255],[EXTREMISM,255,EXTREMISM],
                   [127,127,127], [255,255,255], [255,127,0]
                   ])
DELAY = 8


class Square(object):
    def __init__(self, middle, halfsize):
        self.middle = middle
        self.halfsize = halfsize
        
    def has_point(self, pt):
        ret0 = self.middle[0]-self.halfsize < pt[0] < self.middle[0]+self.halfsize
        ret1 = self.middle[1]-self.halfsize < pt[1] < self.middle[1]+self.halfsize
        return ret0 and ret1

class Gamefield(Entity):
    def __init__(self):
        super(Gamefield, self).__init__()
        
        self.tilemap = {}
        
        self.markone = None
        
    #check whether exchanging markone and marktwo will give any combination
    def first_check(self, marktwo):
        self.swap2tiles(self.markone, marktwo)
        results = self.check_multi_all()
        if results:
            self.scene.sched.add(DELAY, self.initiate_marking, [results])
        else:
            self.swap2tiles(self.markone, marktwo)
            self.scene.inputstop = False
        self.tilemap[self.markone].marked = False
        self.markone = None
        self.scene.combo = 1
    
    def initiate_marking(self, results):
        self.mark_listed(results)
        self.scene.newpoints = COUNTS[0]*COUNTS[1]*len(results)*self.scene.combo
        self.scene.sched.add(DELAY, self.process_match, [results])
        
    def process_match(self, results):
        for i,j in results:
            self.tilemap[(i,j)].delete_content()
        self.scene.sched.add(DELAY,self.check_tiles)
        self.scene.sched.add(DELAY+1, self.add_points)
        #TODO: #if that doesn't work add a defaultarg to check_tiles which allows to call the sched-add at the end
        self.scene.sched.add(DELAY+2,self.check_again)
    
    def add_points(self):
        self.scene.totalpoints += self.scene.newpoints
        self.scene.newpoints = 0
    
    def check_again(self):
        results = self.check_multi_all()
        if results:
            self.scene.sched.add(DELAY, self.initiate_marking, [results])
            self.scene.combo += 1
        else:
            self.scene.inputstop = False
            self.scene.combo = 1
    
    def swap2tiles(self, key1, key2):
        temp = self.tilemap[key1].content
        self.tilemap[key1].set_content(self.tilemap[key2].content)
        self.tilemap[key2].set_content(temp)
    
    def mark_listed(self, listed):
        for l in listed:
            self.tilemap[l].content.lightup = True
    
    def generate_lists(self):
        self.rows = []
        self.cols = []
        for i in range(COUNTS[0]):
            li = []
            for j in range(COUNTS[1]):
                li.append(self.tilemap[(i,j)])        
            self.cols.append(li)
        for j in range(COUNTS[1]):
            li = []
            for i in range(COUNTS[0]):
                li.append(self.tilemap[(i,j)])        
            self.rows.append(li)
        
        
    def check_tiles(self):
        #check if empty or "combination"
        for i in range(COUNTS[0]):
            tofall = []
            fulltiles = 0
            for j in range(COUNTS[1]):
                if self.tilemap[(i,j)].content is not None:
                    if fulltiles != j:
                        tofall.append((fulltiles, j)) #tuple
                    fulltiles += 1
            ### fall down ### 
            for t,f in tofall:
                #if self.tilemap[(i,t)].content is None:
                self.tilemap[(i,t)].set_content(self.tilemap[(i,f)].content)
                self.tilemap[(i,f)].free_content()
            ### if top: generate new gems ###
            for n in range(fulltiles, COUNTS[1]):
                gem = Gemstone(self.tilemap[(i,n)], tier = random.randint(0,STARTTIERS))
                self.scene.add(gem)

    #checks whether there are any 3-combinations and randomizes the gemfield otherwise
    def check_multi_all(self, begintest = False):
        #check individually from "every" tile's content whether the four neighbouring tiles have the same tier
        returning = set()
        for i in range(COUNTS[0]):
            for j in range(COUNTS[1]-2):
                a = self.tilemap[(i,j)].content.tier
                if self.tilemap[(i,j+1)].content.tier == a and self.tilemap[(i,j+2)].content.tier == a:
                    if begintest:
                        return True
                    else:
                        returning.update([(i,j), (i,j+1), (i,j+2)])
                        for n in range(3, COUNTS[1]-j):
                            if self.tilemap[(i,j+n)].content.tier == a:
                                returning.add((i,j+n))
                            else:
                                break
        
        for i in range(COUNTS[0]-2):
            for j in range(COUNTS[1]):
                a = self.tilemap[(i,j)].content.tier
                if self.tilemap[(i+1,j)].content.tier == a and self.tilemap[(i+2,j)].content.tier == a:
                    if begintest:
                        return True
                    else:
                        returning.update([(i,j), (i+1,j), (i+2,j)])
                        for n in range(3, COUNTS[0]-i):
                            if self.tilemap[(i+n,j)].content.tier == a:
                                returning.add((i+n,j))
                            else:
                                break
        if begintest:
            return False
        else:
            return returning


    def randomize_fields(self):
        for i in range(COUNTS[0]):
            for j in range(COUNTS[1]):
                self.tilemap[(i,j)].content.change_color(random.randint(0,STARTTIERS))
                

class Tile(Entity):
    def __init__(self, fieldkey, pos, content=None):
        super(Tile, self).__init__()
        self.fieldkey = fieldkey
        self.pos = pos
        self.color = [150,100,150]
        self.content = content
        self.marked = False
        
    def set_content(self, content):
        #content.tile.content = None
        self.content = content
        #if self.content.tile is not self:
        self.content.change_tile(self)
    
    def delete_content(self):
        if self.content is not None:
            self.content.purge()
            self.content = None
    
    def free_content(self):
        self.content = None
        
    
    def create_touchable(self):
        surrounding = [np.array([self.pos, self.pos, self.pos, self.pos])+TILESIZES]
        areas = [Square(self.pos, SIZE)]

        self.touchable = Touchable(self, surrounding = surrounding, areas = areas)
        self.scene.add(self.touchable)

    def draw_main(self):
        #glLoadIdentity()
        if self.marked:
            glLineWidth(1)        
            glBegin(GL_LINE_LOOP)
            glColor3ub(255,255,255)
            for i in TILESIZES:
                glVertex2d(*(self.pos+0.8*i))
            glEnd()
        
        glLineWidth(1)        
        glBegin(GL_LINE_LOOP)
        glColor3ub(*self.color)
        for i in TILESIZES:
            glVertex2d(*(self.pos+i))
        glEnd()

        #glLoadIdentity()


class Gemstone(Entity):
    def __init__(self, tile, tier):
        super(Gemstone, self).__init__()
        
        self.tile = tile
        tile.set_content(self)
        self.pos = tile.pos
        self.tier = tier
        self.color = COLORS[tier]
        self.lightup = False

    def change_tile(self, tile):
        #self.tile.content = None
        self.tile = tile
        self.pos = tile.pos

    def change_color(self, tier):
        self.tier = tier
        self.color = COLORS[tier]

    def draw_main(self):
        magictier = (3+self.tier)
        anglevar = 2*math.pi/magictier
        vect = np.array([0,0.8*SIZE])

        glLineWidth(1)
        if self.lightup:
            glLineWidth(5)
        
        glBegin(GL_LINE_LOOP)
        glColor3ub(*self.color)
        for i in range(magictier):
            mat = np.array([[math.cos(i*anglevar), -math.sin(i*anglevar)],
                            [math.sin(i*anglevar), math.cos(i*anglevar)]])
            
            #glVertex2d(*(self.pos))
            glVertex2d(*((self.pos)+ np.dot(mat, vect)))
            
        glEnd()

        glBegin(GL_LINES)
        glColor3ub(*self.color)
        for i in range(magictier):
            mat = np.array([[math.cos(i*anglevar), -math.sin(i*anglevar)],
                            [math.sin(i*anglevar), math.cos(i*anglevar)]])
            
            glVertex2d(*(self.pos))
            glVertex2d(*((self.pos)+ np.dot(mat, vect)))
            
        glEnd()

class Touchable(Entity):    
    def __init__(self, caller, surrounding, areas, text=None):
        super(Touchable, self).__init__()

        self.surrounding = surrounding
        self.areas = areas
        self.caller = caller
        self.text = text

    def in_area(self, pt):
        if any(ar.has_point(pt) for ar in self.areas):
            return True
        else:
            return False

    
