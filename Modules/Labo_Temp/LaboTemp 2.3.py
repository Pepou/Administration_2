
#-*- coding: utf-8 -*-
from PyQt4 import QtGui
#from PyQt4.QtCore import SIGNAL

from IHM.connexion2 import Connexion
import sys
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = Connexion()
    myapp.show()
    
    sys.exit(app.exec_())
