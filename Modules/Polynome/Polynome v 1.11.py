#-*- coding: utf-8 -*-
from PyQt4 import QtGui
import sys

from GUI.connexion2 import Connexion

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    myapp = Connexion()
    myapp.show()    
    
    sys.exit(app.exec_())

