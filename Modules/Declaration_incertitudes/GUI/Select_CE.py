# -*- coding: utf-8 -*-

"""
Module implementing Select_CE.
"""

from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtGui import QDialog, QTableWidgetItem, QCheckBox

from .Ui_Select_CE import Ui_Select_CE
from PyQt4.QtCore import SIGNAL

class Select_CE(QDialog, Ui_Select_CE):
    """
    Class documentation goes here.
    """
    def __init__(self, generator_poly, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Select_CE, self).__init__(parent)
        self.setupUi(self)
        
#        print(list_poly)
        for ele in reversed(list(generator_poly)) : 
#            print(ele)
            self.tableWidget.insertRow(0)
            
            item_nom_etal = QTableWidgetItem(str(ele[0]))
            item_nom_etal.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.tableWidget.setItem(0, 0, item_nom_etal)
            
            item_date = QTableWidgetItem(str(ele[1]))
            item_date.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.tableWidget.setItem(0, 1, item_date)
           
            item_ce = QTableWidgetItem(str(ele[2]))
            item_ce.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.tableWidget.setItem(0, 2, item_ce)
            
            item_residu = QTableWidgetItem(str(ele[3]))
            item_residu.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            self.tableWidget.setItem(0, 3, item_residu)
            
            check_box = QCheckBox (self.tableWidget)
            self.tableWidget.setCellWidget(0, 4, check_box)
    
    @pyqtSlot()
    def on_okButton_clicked(self):
        """
        Slot documentation goes here.
        """
        nbr_ligne = self.tableWidget.rowCount()
        list_ce = [] 
        for ligne in range(nbr_ligne):
            if self.tableWidget.cellWidget(ligne, 4).isChecked():
                etalon = self.tableWidget.item(ligne, 0).text()
                date = self.tableWidget.item(ligne, 1).text()
                n_ce = self.tableWidget.item(ligne, 2).text()
                
                list_ce.append((etalon, date, n_ce))
                
        self.emit(SIGNAL("fermetureSelect_CE(PyQt_PyObject)"), list_ce)
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
