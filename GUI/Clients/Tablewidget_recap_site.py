#from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import  Qt, SIGNAL, pyqtSignal
from PyQt4.QtGui import QTableWidget
#import sys

class Tablewidget_Recap_Site(QTableWidget):
    
    signalSelect_site = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(Tablewidget_Recap_Site, self).__init__(parent)
#        print("nb ligne {}".format(self.rowCount()))

    
    def mouseDoubleClickEvent(self, event):
        """gestion du copier coller dans le tableau homogeneite"""
        
#        print(event)       
        if event.button() == Qt.LeftButton:
#            print("cebfrjzefjkrer")
            ligne = self.currentRow()

            self.signalSelect_site.emit(ligne)
    
    
    def keyPressEvent(self, event):
        key = event.key()
#        print(key)
        if key == Qt.Key_Delete or key == Qt.Key_Backspace:
            ligne_select = self.currentRow()
            
            if ligne_select != -1 :
                self.removeRow(ligne_select)
