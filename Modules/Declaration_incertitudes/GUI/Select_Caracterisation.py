# -*- coding: utf-8 -*-

"""
Module implementing Select_Caracterisation.
"""

from PyQt4.QtCore import pyqtSlot, Qt, SIGNAL
from PyQt4.QtGui import QDialog, QTableWidgetItem, QCheckBox

from .Ui_Select_Caracterisation import Ui_Select_Caracterisation


class Select_Caracterisation(QDialog, Ui_Select_Caracterisation):
    """
    Class documentation goes here.
    """
    def __init__(self, list_caracterisation, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Select_Caracterisation, self).__init__(parent)
        self.setupUi(self)
        
        for ele in reversed(list_caracterisation) : 
            self.tableWidget.insertRow(0)
            item_date = QTableWidgetItem(str(ele[1]))
            item_date.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.tableWidget.setItem(0, 0, item_date)
           
            item_carac = QTableWidgetItem(str(ele[0]))
            item_carac.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.tableWidget.setItem(0, 1, item_carac)
            
            item_nom_gene = QTableWidgetItem(str(ele[3]))
            item_nom_gene.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.tableWidget.setItem(0, 2, item_nom_gene)
            
            item_u = QTableWidgetItem(str(ele[2]))
            item_u.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.tableWidget.setItem(0, 3, item_u)
            
            
            check_box = QCheckBox (self.tableWidget)
            self.tableWidget.setCellWidget(0, 4, check_box)
    
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        nbr_ligne = self.tableWidget.rowCount()
        caracterisation = []
        for ligne in range(nbr_ligne):
            if self.tableWidget.cellWidget(ligne, 4).isChecked():
                tupple =(self.tableWidget.item(ligne, 0).text(), self.tableWidget.item(ligne, 1).text())
                caracterisation.append(tupple)
        self.emit(SIGNAL("fermetureSelect_Caracterisation(PyQt_PyObject)"), caracterisation)
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
