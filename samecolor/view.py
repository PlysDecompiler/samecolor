# Game: "Samecolor"
# Author: Thomas Strenger

from PySide.QtOpenGL import QGLWidget
from samecolor.opengl import *
from samecolor.entity import *
from PySide.QtGui import QFont
from PySide.QtCore import QRect

class Viewport(QGLWidget):
    def __init__(self, perspective, parent=None):
        super(Viewport, self).__init__(parent)
        self.perspective = perspective
    
    def initializeGL(self):     pass    
    def resizeGL(self, w, h):   self.perspective.viewport_resized(w, h)
    def paintGL(self):          self.perspective.draw(self)        
    
            
class MainPerspective(object):
    def __init__(self, scene):
        self.scene = scene
    
    def setup(self):
        glLoadIdentity()
        glScale(0.01,0.01,0.01)
        glTranslate(-BIGSIZE*COUNTS[0], -BIGSIZE*COUNTS[1],0)

    def viewport_resized(self, width, height):
        side = min(width, height)
        glViewport((width - side) / 2, (height - side) / 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-100, 100, -100, 100, -100.0, 100.0);
        
    def draw(self, viewport):
        self.setup()
        
        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  
            
        for a in self.scene.iter_instances(Tile):
            a.draw_main()
        for a in self.scene.iter_instances(Gemstone):
            a.draw_main()            
            
        glColor3ub(255,255,255)
        myFont = QFont("Console", 20)
        viewport.renderText(110.0,30.0,str(self.scene.totalpoints),myFont)
        myFont = QFont("Console", 15)
        viewport.renderText(110.0,50.0,'+' + str(self.scene.newpoints),myFont)
        myFont = QFont("Console", 25)
        viewport.renderText(310.0,40.0,'CHAIN ' + str(self.scene.combo),myFont)
            
            
            
            
