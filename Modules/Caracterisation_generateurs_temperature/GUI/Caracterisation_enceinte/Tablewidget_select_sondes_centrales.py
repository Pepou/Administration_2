from PyQt4 import QtGui, QtCore
import sys

class Tablewidget_select_sondes_centrales(QtGui.QTableWidget):

    def __init__(self, parent=None):
        super(Tablewidget_select_sondes_centrales, self).__init__(parent)
        
        self.insertRow(0)

    def mouseReleaseEvent(self, event):
        """ recuper un clic droit de la souris sur le tablewidget et demande a la fct rightclickmenu de fct"""
        if event.button() == QtCore.Qt.RightButton:
            self.rightClickMenu(event)   
        
    def rightClickMenu(self,  event):       
        """definition du menu et de sa position"""
        
        self.mapToGlobal(QtCore.QPoint(0, 0)) 
        menu = QtGui.QMenu(self)
        select = menu.addAction("Selectionner toutes les sondes")
        deselect = menu.addAction("Deselectionner toutes les sondes")
        
        select.triggered.connect(self.select_sondes)
        deselect.triggered.connect(self.deselect_sondes)

        pos = event.pos()

        menu.popup( self.mapToGlobal(pos) ) #maptoglobal position permete de definir la position (0,,0) sur le qwideget et non sur windows
    
    def select_sondes(self):
        """ Fct qui coche l'ensemble des checkbox representant les sondes des borniers centrales"""
        nb_ligne =self.rowCount()
        for i in range(nb_ligne):
            self.cellWidget(i, 1).setChecked(True)
        
    def deselect_sondes(self):
        """fct qui decoche les checkbox representant les sondes borniers centrales"""
        nb_ligne =self.rowCount()
        for i in range(nb_ligne):
            self.cellWidget(i, 1).setChecked(False)
