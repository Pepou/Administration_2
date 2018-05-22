# -*- coding: utf-8 -*-

"""
Module implementing Select_Etalon.
"""

from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtGui import QDialog,  QTableWidgetItem, QCheckBox

from .Ui_Select_Etalons import Ui_Select_Etalon
from PyQt4.QtCore import SIGNAL

class Select_Etalon(QDialog, Ui_Select_Etalon):
    """
    Class documentation goes here. """
    def __init__(self, list_etalon, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Select_Etalon, self).__init__(parent)
        self.setupUi(self)
        
#        list_etalon.sort()
        
        for ele in list_etalon : 
            self.tableWidget.insertRow(0)
            item_etalon = QTableWidgetItem(str(ele))
            item_etalon.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled)
            self.tableWidget.setItem(0, 0, item_etalon)
            
            check_box = QCheckBox (self.tableWidget)
            self.tableWidget.setCellWidget(0, 1, check_box)
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        nbr_ligne = self.tableWidget.rowCount()
        nom_etalons = []
        for ligne in range(nbr_ligne):
            if self.tableWidget.cellWidget(ligne, 1).isChecked():
                nom_etalons.append(self.tableWidget.item(ligne, 0).text())
        self.emit(SIGNAL("fermetureSelect_Etalon(PyQt_PyObject)"), nom_etalons)
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
