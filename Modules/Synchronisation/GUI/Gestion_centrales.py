# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt4.QtGui import QStandardItemModel, QStandardItem 
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog

from PyQt4 import QtGui

from .Ui_Gestion_centrales import Ui_Dialog
from PyQt4.QtCore import SIGNAL
from Modules.Synchronisation.GUI.extendedcombo import ExtendedCombo



class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, identifications, parc, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.identifications = identifications
#        print(identifications)
        
        for ident in reversed(self.identifications):
            self.tableWidget_instrument.insertRow(0)
            item = QtGui.QTableWidgetItem()
            self.tableWidget_instrument.setVerticalHeaderItem(0, item)
            item.setText(str(ident))
        
        self.tableWidget_instrument.insertColumn(0)
        
        parc.insert(0,"*")
        for ligne in range(len(self.identifications)):
            
            combobox = ExtendedCombo()
            combobox.installEventFilter(self)
            model = QStandardItemModel()
        
            

            for i,word in enumerate(parc):
                item = QStandardItem(word)
                model.setItem(i, 0, item)

            combobox.setModel(model)
            combobox.setModelColumn(0)
            
            self.tableWidget_instrument.setCellWidget(ligne, 0, combobox)
            
        for ligne in range(len(self.identifications)):
            self.tableWidget_instrument.cellWidget(ligne, 0).setCurrentIndex(0)

            
#        print("nbr ligne tableau {}".format(self.tableWidget_instrument.rowCount()))
        
  
    
    @pyqtSlot()
    def on_pushButton_ok_clicked(self):
        """
        Slot documentation goes here.
        """
        dict_ident_sondes= {}
        for i in range(len(self.identifications)):

            dict_ident_sondes[self.tableWidget_instrument.verticalHeaderItem(i).text()]= self.tableWidget_instrument.cellWidget(i, 0).currentText()
                
        self.emit(SIGNAL("fermetureGestionCentrales(PyQt_PyObject)"), dict_ident_sondes)
        
        self.close()
    
    @pyqtSlot()
    def on_pushButton__annule_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
