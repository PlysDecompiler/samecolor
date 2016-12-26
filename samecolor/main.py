"""
Main module of this package call main with commandline parameters (which get passed to Qt)
or execute the csis application module which does this for you.
"""

import sys
from PySide.QtGui   import QApplication
from samecolor.game import *


def main(argv):
    app = QApplication(argv)
    iw = Game()
    iw.show()
    
    sys.exit(app.exec_())
    
    