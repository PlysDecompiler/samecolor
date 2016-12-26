# Game: "Samecolor"
# Author: Thomas Strenger
#
#

from PySide.QtCore import Qt
from collision import mousepos_to_gamepos, gamepos_to_mousepos

from entity import BIGSIZE, COUNTS

class Director(object):
    """
    Directs the Actors to act according to some kind of script which may be based on user input.
    The actors are part of the scene and identified as actors by their description in the script.
    Makes the actors execute according to script.    (script interpreter)
    """
    def __init__(self, scene, script):
        self.scene      = scene
        self.script     = script
        
        #keys and buttons that shall be able to be pressed continuosly
        self.key_filter = set([Qt.Key_Left, Qt.Key_Right, Qt.Key_Down, Qt.Key_Up,
                               Qt.Key_Space, Qt.Key_PageDown, Qt.Key_PageUp])
        self.button_filter = set([Qt.LeftButton, Qt.MidButton, Qt.RightButton])
        
        self.is_down    = set()
        
    def key_down(self, event):
        key = event.key()
        
        if key == Qt.Key_R:
            pass

        if key in self.key_filter:
            self.is_down.add(key)
        
    def key_up(self, event):
        key = event.key()
        self.is_down.discard(key)
        

    def mouse_down(self, event):
        button = event.button()
        
        pos = [event.x(), event.y()]
        if button == Qt.LeftButton:
            newPos = mousepos_to_gamepos(pos, playerpos=(BIGSIZE*COUNTS[0], BIGSIZE*COUNTS[1]), mS = self.scene.maxHeight)
            
            self.scene.game.handle_click(newPos)
                                        
        
        if button in self.button_filter:
            self.is_down.add(button)    
    
    def mouse_up(self, event):             
        button = event.button()
        
        self.is_down.discard(button)    

    def mouse_move(self, event):
        pos = event.pos()

  
    def animation_step(self):
        
        if Qt.Key_Left in self.is_down:
            pass

        
class Actor(object):
    """
    provides actions, acted out according to Script, directed by the Director.
    
    TODO
    reason about different types of actions, and how they can be "told" by the director
    timing etc.
    """
    pass

    
class Script(object):
    """
    Describes a set of entities and how they act upon another
    """
    pass

