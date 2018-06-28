from PyQt4.QtCore import  Qt,  pyqtSignal
from PyQt4.QtGui import  QTableWidget, QMenu
#import sys
#import pandas as pd
class TableWidget_Recap(QTableWidget):
    
    ligne_clic = pyqtSignal(int)
    annule_et_remplace = pyqtSignal(int)
    nouvelle = pyqtSignal()
    
    def __init__(self, parent=None):
        super(TableWidget_Recap, self).__init__(parent)
        
        
    def mouseDoubleClickEvent(self, event):
        """gestion du copier coller dans le tableau homogeneite"""
        
#        print(event)
       
        if event.button() == Qt.LeftButton:

#            print("o putain tu sais programme toi")
#            items_tableView = self.selectedIndexes()
#            print(str(self.currentRow()))
            
            self.ligne_clic.emit(self.currentRow())
    
    def mousePressEvent(self, event):
#        print(event.pos())
#        print("pipe")
        if event.button() == Qt.RightButton:
            try:
                ligne = self.itemAt(event.pos()).row()
                self.selectRow(ligne)
                
                menu = QMenu(self)
                nouvelle = menu.addAction("Nouvelle Cartographie")
                modification = menu.addAction("Visualisation/Modification Cartographie")
                annule = menu.addAction("Annule et Remplace Cartographie")
                action = menu.exec_(event.globalPos())                
                
                if action == annule:                
                    self.annule_et_remplace.emit(ligne)
                elif action == modification:
                    self.ligne_clic.emit(ligne)
                elif action == nouvelle:                
                    self.nouvelle.emit()
            
            except:
                pass
                
        elif event.button() == Qt.LeftButton:
            try:            
                ligne = self.itemAt(event.pos()).row()                
                self.selectRow(ligne)
            except:
                pass
            
            
            
            
