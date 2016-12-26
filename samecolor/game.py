# Game: "Samecolor"
# Author: Thomas Strenger

import random

from PySide.QtCore import QTimer, Qt
from PySide.QtGui import QApplication, QWidget, QDesktopWidget

from samecolor.view import Viewport, MainPerspective
from samecolor.world import Scene
from samecolor.entity import *
from samecolor.animation import Director
from samecolor.scheduler import *
        
import math

    
class Game(QWidget):
    time = 0
    
    def keyPressEvent(self, event):     self.director.key_down(event)
    def keyReleaseEvent(self, event):   self.director.key_up(event)
    def mousePressEvent(self, event):   self.director.mouse_down(event)
    def mouseReleaseEvent(self, event): self.director.mouse_up(event)
    def mouseMoveEvent(self, event):    self.director.mouse_move(event)
    
    def __init__(self, parent=None):
        super(Game, self).__init__(parent)
        self.setWindowTitle(self.tr("Samecolor"))

        tempdesktop = QApplication.desktop() 
        
        self.maxWidth = (tempdesktop.screenGeometry().width()/100)*100
        self.maxHeight = (tempdesktop.screenGeometry().height()/100)*100

        self.viewwidth = self.maxHeight 
        self.viewheight = self.maxHeight 
        
        if self.viewheight > self.maxWidth:
            self.viewwidth = self.maxWidth                                                  

        self.setGeometry(0,0,self.viewwidth,self.viewheight)

        self.setMouseTracking(True)  
        
        self.scene      = Scene()
        self.director   = Director(self.scene, None)
        
        self.scene.game = self
        
        self.setFocusPolicy(Qt.StrongFocus)      
        self.scene.maxHeight = float(self.maxHeight)

        self.main_view = Viewport(MainPerspective(self.scene), self)
        self.main_view.setGeometry(2,2,self.maxHeight,self.maxHeight)
        self.main_view.setMouseTracking(True)
        
        self.scene.gamefield = Gamefield()
        self.scene.add(self.scene.gamefield)
        
        self.generate_field()
        
        self.scene.inputstop = False
        
        self.scene.totalpoints = 0
        self.scene.newpoints = 0
        self.scene.combo = 1
        self.scene.level = 1
        self.scene.xp = 0
        
        # start timer
        self.scene.time = 0
        self.scene.sched = Scheduler(self.scene.time)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timestep)
        self.timer.start(10)
        
    def generate_field(self):
        for i in range(COUNTS[0]):
            for j in range(COUNTS[1]):
                tile = Tile(fieldkey = (i,j), pos = np.array([2*BIGSIZE*i,2*BIGSIZE*j]) )
                self.scene.add(tile)
                
                tile.create_touchable()
                self.scene.gamefield.tilemap[(i,j)] = tile
                gem = Gemstone(tile, tier = random.randint(0,STARTTIERS))
                self.scene.add(gem)
                
        while self.scene.gamefield.check_multi_all(begintest = True):
            self.scene.gamefield.randomize_fields()

    def handle_click(self, point):
        if not self.scene.inputstop:
            for touchable in self.scene.iter_instances(Touchable):
                if touchable.in_area(point):
                    touchable.caller.color = tuple(255-fc for fc in touchable.caller.color)
                    if self.scene.gamefield.markone is None:
                        self.scene.gamefield.markone = touchable.caller.fieldkey
                        touchable.caller.marked = True
                    else:
                        self.scene.inputstop = True
                        self.scene.gamefield.first_check(touchable.caller.fieldkey)


    def timestep(self):
        self.scene.time += 1
        self.scene.sched.set_time(self.scene.time)
        self.scene.sched.execute()
        #if not self.scene.time % 10:
        self.timedHappenings()
        
    def timedHappenings(self):
        self.director.animation_step()
                           
                        
        self.main_view.updateGL()


