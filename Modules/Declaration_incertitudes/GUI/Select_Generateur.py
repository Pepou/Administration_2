# -*- coding: utf-8 -*-

"""
Module implementing Select_Generateurs.
"""

from PyQt4.QtCore import pyqtSlot, Qt, SIGNAL
from PyQt4.QtGui import QDialog, QTableWidgetItem, QCheckBox

from .Ui_Select_Generateur import Ui_Select_Generateurs


class Select_Generateurs(QDialog, Ui_Select_Generateurs):
    """
    Class documentation goes here.
    """
    def __init__(self, list_generateurs, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Select_Generateurs, self).__init__(parent)
        self.setupUi(self)
        
        for ele in list_generateurs : 
            self.tableWidget.insertRow(0)
            item_etalon = QTableWidgetItem(str(ele))
            item_etalon.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.tableWidget.setItem(0, 0, item_etalon)
            
            check_box = QCheckBox (self.tableWidget)
            self.tableWidget.setCellWidget(0, 1, check_box)
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        nbr_ligne = self.tableWidget.rowCount()
        nom_generateurs = []
        for ligne in range(nbr_ligne):
            if self.tableWidget.cellWidget(ligne, 1).isChecked():
                nom_generateurs.append(self.tableWidget.item(ligne, 0).text())
        self.emit(SIGNAL("fermetureSelect_Generateurs(PyQt_PyObject)"), nom_generateurs)
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
