from PyQt4.QtCore import  Qt,  pyqtSignal
from PyQt4.QtGui import  QTableWidget
#import sys
#import pandas as pd
class TableWidget_Recap(QTableWidget):
    
    ligne_clic= pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(TableWidget_Recap, self).__init__(parent)
        
        
    def mouseDoubleClickEvent(self, event):
        """gestion du copier coller dans le tableau homogeneite"""
        
        print(event)
       
        if event.button() == Qt.LeftButton:

#            print("o putain tu sais programme toi")
            items_tableView = self.selectedIndexes()
#            print(str(self.currentRow()))
            
            self.ligne_clic.emit(self.currentRow())
#
#        clavier = event.key()
#
#        if items_tableView !=None:
#            if clavier == 67 :
#                self.copySelection()
